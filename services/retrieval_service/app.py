import os
import logging
from typing import List
from dotenv import find_dotenv, load_dotenv

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import openai
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from insert_data import _create_collection

ROLE_CLASS_MAP = {
    "assistant": AIMessage,
    "user": HumanMessage,
    "system": SystemMessage
}

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = "postgresql+psycopg2://admin:admin@postgres:5432/vectordb"
COLLECTION_NAME="vectordb"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    conversation: List[Message]

embeddings = OpenAIEmbeddings()
chat = ChatOpenAI(temperature=0)
store = PGVector(
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
    embeddings=embeddings,
)
retriever = store.as_retriever()

prompt_template = """As a FAQ Bot for the Llama 3 Technical Report, you have been given the following information:

{context}

Please provide the most suitable response for the users question.
Answer:"""

prompt = PromptTemplate(
    template=prompt_template, input_variables=["context"]
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)


def create_messages(conversation):
    return [ROLE_CLASS_MAP[message.role](content=message.content) for message in conversation]


def format_docs(docs):
    formatted_docs = []
    for doc in docs:
        formatted_doc = "Source: " + doc.metadata['source']
        formatted_docs.append(formatted_doc)
    return '\n'.join(formatted_docs)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "This is the retrieval service's root!"}

@app.on_event("startup")
async def startup_event():
    """To ensure that the collections are created at startup"""
    _create_collection()

@app.post("/retrieval_service/{conversation_id}")
async def retrieval_service(conversation_id: str, conversation: Conversation):

    query = conversation.conversation[-1].content

    docs = retriever.similarity_search(query=query, k=3)
    docs = format_docs(docs=docs)

    prompt = system_message_prompt.format(context=docs)
    messages = [prompt] + create_messages(conversation=conversation.conversation)

    result = chat(messages)

    return {"id": conversation_id, "reply": result.content}