import os
import logging
from glob import glob
from sys import stdout
from dotenv import find_dotenv, load_dotenv

from sqlalchemy.orm import Session

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_unstructured import UnstructuredLoader

logger = logging.getLogger('__main__.' + __name__)

logger.setLevel(logging.INFO)
logFormatter = logging.Formatter\
("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

load_dotenv(find_dotenv())

def _create_collection():
    """
    Creates or retrieves a vector database collection using PGVector and OpenAI embeddings.

    This function establishes a connection to a PostgreSQL database using environment variables
    (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`). It then attempts to retrieve an existing
    collection from PGVector. If the collection does not exist, it loads documents from PDF files 
    in the `data/` directory using the UnstructuredLoader and populates the collection with embeddings.

    Dependencies:
        - OpenAIEmbeddings for generating text embeddings.
        - PGVector for storing and retrieving vector embeddings.
        - UnstructuredLoader for loading text data from PDF files.
        - psycopg2 for PostgreSQL connection.

    Environment Variables:
        - POSTGRES_DB: Name of the PostgreSQL database.
        - POSTGRES_USER: Database username.
        - POSTGRES_PASSWORD: Database password.
        - UNSTRUCTURED_API_KEY: API key for document processing.

    Side Effects:
        - Prints a message if the collection already exists.
        - Loads and embeds documents if the collection is not found.
    """
    embeddings = OpenAIEmbeddings()

    dbname = os.environ.get('POSTGRES_DB')
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')

    # PGVector needs the connection string to the database.
    CONNECTION_STRING = f"postgresql+psycopg2://{user}:{password}@postgres:5432/{dbname}"
    COLLECTION_NAME = dbname

    pgvector = PGVector(
        embeddings=OpenAIEmbeddings(),
        collection_name=dbname,
        connection=CONNECTION_STRING
    )

    with Session(pgvector._engine) as session:
        docs = session.query(pgvector.EmbeddingStore.document).all()
        logger.info(f"No. of docs: {len(docs)}")

    if  len(docs) != 0:
        logger.info(f"{len(docs)} have already been upserted")
    else:
        logger.info(f"No documents have been upserted. Will proceed to load documents and build indexes.")
        loader = UnstructuredLoader(
            file_path=[f for f in glob("data/*.pdf")],
            api_key=os.getenv("UNSTRUCTURED_API_KEY"),
            partition_via_api=True,
        )

        docs = loader.load()

        pgvector.from_documents(
            docs,
            embeddings,
            collection_name=COLLECTION_NAME,
            connection=CONNECTION_STRING
        )

if __name__ == "__main__":
    _create_collection()
