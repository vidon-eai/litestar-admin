from typing import TYPE_CHECKING

from langchain_ollama import ChatOllama, OllamaEmbeddings

if TYPE_CHECKING:
    from .config import RAGConfig


class RAGService:
    def __init__(self, config: "RAGConfig"):
        print("RAGService initialized with config:", config)
        self.config = config
        self.llm = ChatOllama(model=config.llm_model)
        self.embeddings = OllamaEmbeddings(model=config.embedding_model)

    def chat(self, prompt: str):
        messages = [
            ("human", prompt),
        ]

        return self.llm.invoke(messages)

    def embed_query(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)
