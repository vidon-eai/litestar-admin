from typing import TYPE_CHECKING

from app.db.models.dataset import Dataset
from app.plugins.rag.vector_store.milvus_vector import VectorFactory
from app.plugins.rag.vector_store.vertor_factory import Vector
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_ollama import OllamaEmbeddings

if TYPE_CHECKING:
    from .config import RAGConfig


URI = "http://localhost:19530"


DOCS_BASE = "https://docs.langchain.com"

# Curated LangChain OSS pages for this tutorial. Expand this list or parse
# URLs from https://docs.langchain.com/llms.txt to index more of the site.
DOC_PATHS = [
    "oss/python/langchain/agents",
    "oss/python/deepagents/rag",
    "oss/python/langchain/tools",
    "oss/python/langchain/models",
    "oss/python/deepagents/retrieval",
    "oss/python/langchain/knowledge-base",
    "oss/python/langchain/middleware",
    "oss/python/deepagents/overview",
    "oss/python/deepagents/subagents",
    "oss/python/deepagents/streaming",
    "oss/python/deepagents/frontend/subagent-streaming",
    "oss/python/deepagents/backends",
    "oss/python/langgraph/overview",
    "oss/python/langgraph/quickstart",
]


class RAGService:
    llm_provider: str = "ollama:qwen2.5:7b-instruct-q4_K_M"

    def __init__(self, config: "RAGConfig"):
        print(config)
        self.config = config
        self._embeddings = OllamaEmbeddings(model=config.embedding_model)
        # self._init_milvus_database()

    def get_embedding(self, provider: str) -> OllamaEmbeddings:
        return OllamaEmbeddings(model=provider)

    def _get_llm(self, provider: str):
        return init_chat_model(model=provider, temperature=0)

    async def embed(self, dataset: Dataset, docs: list[Document], index_ids: list[str]):
        # vector_factory = VectorFactory()
        # vector_store = vector_factory.init_vector(
        #     collection_name=collection_name, embeddings=self._embeddings
        # )

        vertor = Vector(dataset=dataset, embedding_model="qwen3-embedding:8b")
        return await vertor.aadd_documents(docs, index_ids=index_ids)

    def delete_collection(self, collection_name: str):
        vector_factory = VectorFactory()
        vector_store = vector_factory.init_vector(
            collection_name=collection_name, embeddings=self._embeddings
        )
        vector_store.delete_collection()

    def delete_documents(self, collection_name: str, index_ids: list[str]):
        vector_factory = VectorFactory()
        vector_store = vector_factory.init_vector(
            collection_name=collection_name, embeddings=self._embeddings
        )

        return vector_store.delete_documents(index_ids=index_ids)

    async def search(self, query: str, collection_name: str):
        vector_factory = VectorFactory()
        vector_store = vector_factory.init_vector(
            collection_name=collection_name, embeddings=self._embeddings
        )
        return await vector_store.asimilarity_search_with_score(query, k=4)

    async def chat(self, prompt: str, dataset: Dataset, provider: str):
        try:
            # vector_factory = VectorFactory()
            # vector_store = vector_factory.init_vector(
            #     collection_name=collection_name, embeddings=self._embeddings
            # )

            vector = Vector(dataset=dataset, embedding_model="qwen3-embedding:8b")
            retriever = vector.as_retriever(
                search_type="similarity",  # Could also use "mmr" for diversity
                search_kwargs={"k": 4},
            )

            # retriever = vector_store.get_vector_store().as_retriever(
            #     search_type="similarity",  # Could also use "mmr" for diversity
            #     search_kwargs={"k": 4},
            # )

            retriever_tool = retriever.as_tool(
                name="knowledge_base_search",
                description="用於搜尋企業內部知識庫，回答相關領域問題前必須先查詢此工具。",
            )

            system_prompt = """你是一個專業的知識庫回答助手。

                請遵循以下思考與檢索原則：
                1. 當使用者提出的問題需要參考內部文件時，優先調用 `knowledge_base_search` 工具。
                2. 檢索結果傳回後，評估資訊是否充足。如果檢索到的資訊不足以回答問題，直接回答查找不到相關內容。
                3. 請嚴格根據檢索到的上下文資訊回答，切勿虛構或編造未發生的事實。
                4. 回答完畢後，請簡單列出參考資料的來源。
                """

            agent = create_agent(
                model=self._get_llm(provider),
                tools=[retriever_tool],
                system_prompt=system_prompt,
            )

            response = await agent.ainvoke({"messages": [HumanMessage(content=prompt)]})

            return response

        except Exception as e:
            print(f"Error during chat: {e}")
            raise
