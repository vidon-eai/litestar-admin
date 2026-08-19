from typing import TYPE_CHECKING

from app.db.models.dataset import Dataset
from app.plugins.rag.vector_store.vertor_factory import Vector
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_ollama import OllamaEmbeddings

if TYPE_CHECKING:
    from .config import RAGConfig


class RAGService:
    llm_provider: str = "ollama:qwen2.5:7b-instruct-q4_K_M"

    def __init__(self, config: "RAGConfig"):
        print(config)
        self.config = config
        self._embeddings = OllamaEmbeddings(model=config.embedding_model)
        self._embedding_model = "bge-m3:latest"

    def get_embedding(self, provider: str) -> OllamaEmbeddings:
        return OllamaEmbeddings(model=provider)

    def _get_llm(self, provider: str):
        return init_chat_model(model=provider, temperature=0)

    async def embed(self, dataset: Dataset, docs: list[Document], index_ids: list[str]):
        vertor = Vector(dataset=dataset, embedding_model=self._embedding_model)
        return await vertor.aadd_documents(docs, index_ids=index_ids)

    def delete_collection(self, dataset: Dataset):

        vector_store = Vector(dataset=dataset, embedding_model=self._embedding_model)
        vector_store.delete_collection()

    async def chat(self, prompt: str, dataset: Dataset, provider: str):
        try:
            vector = Vector(dataset=dataset, embedding_model=self._embedding_model)
            retriever = vector.as_retriever(
                search_type="similarity",  # Could also use "mmr" for diversity
                search_kwargs={"k": 4},
            )

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
