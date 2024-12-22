import os
from glob import glob
from dotenv import find_dotenv, load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_unstructured import UnstructuredLoader

load_dotenv(find_dotenv())

def _create_collection():
    embeddings = OpenAIEmbeddings()

    loader = UnstructuredLoader(
        file_path=[f for f in glob("data/*.pdf")],
        api_key=os.getenv("UNSTRUCTURED_API_KEY"),
        partition_via_api=True,
    )

    docs = loader.load()

    # PGVector needs the connection string to the database.
    CONNECTION_STRING = "postgresql+psycopg2://admin:admin@postgres:5432/vectordb"
    COLLECTION_NAME = "vectordb"

    PGVector.from_documents(
        docs,
        embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING
    )

if __name__ == "__main__":
    _create_collection()
