from typing import TYPE_CHECKING

from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.runnables.config import RunnableConfig
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

if TYPE_CHECKING:
    from .config import RAGConfig


class RAGService:
    def __init__(self, config: "RAGConfig"):
        self.config = config
        self.llm = init_chat_model(temperature=0)
        self.embeddings = OllamaEmbeddings(model=config.embedding_model)

    def model_config(self, provider: str) -> RunnableConfig:
        if not provider:
            raise ValueError("Please select a model provider for the LLM model.")
        return RunnableConfig(model=provider)

    async def add_docs(self, collection: str):

        self.vector_store = PGVector(
            connection=self.config.postgres_connection_string,
            collection_name=collection,
            embeddings=self.embeddings,
            async_mode=True,
            create_extension=False,  # Disable automatic extension creation
        )
        docs = [
            Document(
                page_content="there are cats in the pond",
                metadata={"id": 1, "location": "pond", "topic": "animals"},
            ),
        ]

        await self.vector_store.aadd_documents(
            docs, ids=[doc.metadata["id"] for doc in docs]
        )

    async def chat(self, prompt: str, model_provider: str):
        try:
            messages = [
                ("human", prompt),
            ]

            return await self.llm.ainvoke(
                messages,
                self.model_config(model_provider),
            )
        except Exception as e:
            print(f"Error during chat: {e}")
            raise

    def embed_query(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)
