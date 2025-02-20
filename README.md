This is a RAG Microservice Backend built using **Redis** (to cache conversations), **Postgres/pgvector** (as the vector store),
the [Unstructured](https://docs.unstructured.io/welcome) library (to aid in table/image extraction in PDFs), **LangChain**, **OpenAI API**, and **FastAPI**.

For dummy documents to be ingested into the vector store, we ingest the [Llama 3 Technical Report](https://arxiv.org/abs/2407.21783) and [GPT4All Model Family Introduction](https://arxiv.org/abs/2311.04931) PDFs.

### To start the app
Make sure you've got Docker installed on your system, as well as your OpenAI and Unstructured (optional) API keys!

```{bash}
docker compose up --build
```

### Project Structure
```
.
├── README.md
├── docker-compose.yml
├── notebooks
│   ├── lanchain-practice.ipynb
│   ├── pgvector-practice.ipynb
│   ├── requirements-notebook.txt
│   └── unstructured-practice.ipynb
├── postgres
│   ├── Dockerfile
│   └── init.sql
└── services
    ├── cache_service
    │   ├── Dockerfile
    │   ├── app.py
    │   └── requirements.txt
    └── retrieval_service
        ├── Dockerfile
        ├── app.py
        ├── data
        │   ├── gpt4all.pdf
        │   └── llama3technicalreport.pdf
        ├── insert_data.py
        ├── requirements.txt
        └── wait-for-postgres.sh
```

### Resources
- https://yes-we-can-devops.hashnode.dev/docker-entrypoint-initdbd
- https://stackoverflow.com/questions/53481088/poppler-in-path-for-pdf2image
- https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i
- Logging: https://stackoverflow.com/questions/50714316/how-to-use-logging-getlogger-name-in-multiple-modules
- Logging for Docker: https://gist.github.com/oseme-techguy/8dc90d1808174fc4899bce448ea0e5de
- Unstructured library tutorials: https://www.youtube.com/playlist?list=PLz-qytj7eIWXyYDZuFI89w8WE-pcwI06d
- LangChain Crashcourse (2024): https://www.youtube.com/watch?v=-maRNgjEvLU
- LangChain Runnables: https://www.youtube.com/watch?v=pJ0B_3x0RkU
- Prompt Engineering primer: https://towardsdatascience.com/how-i-won-singapores-gpt-4-prompt-engineering-competition-34c195a93d41
- Pgvector practical guide: https://www.youtube.com/watch?v=PuHP3kktmQI
- Pgvector practical guide (notebook): https://github.com/dmagda/openai-cookbook/blob/main/examples/vector_databases/postgresql/getting_started_with_postgresql_pgvector.ipynb
- PGVector get num. documents in a collection: https://stackoverflow.com/questions/78945858/is-there-any-method-in-langchain-pgvector-to-search-for-all-documents-in-a-colle
