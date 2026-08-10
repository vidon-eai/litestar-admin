import asyncio
from typing import TYPE_CHECKING

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.runnables.config import RunnableConfig
from langchain_milvus import Milvus
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
    def __init__(self, config: "RAGConfig"):
        self.config = config
        self.llm = init_chat_model(
            model="ollama:qwen2.5:7b-instruct-q4_K_M", temperature=0
        )
        self.embeddings = OllamaEmbeddings(model=config.embedding_model)
        self._init_milvus_database()

    def get_vector_store(self, collection: str) -> Milvus:
        vector_store = Milvus(
            embedding_function=self.embeddings,
            connection_args={
                "uri": URI,
                "token": "root:Milvus",
                "db_name": "milvus_demo",
            },
            collection_name=collection,
            index_params={"index_type": "FLAT", "metric_type": "L2"},
            consistency_level="Strong",
            drop_old=False,  # set to True if seeking to drop the collection with that name if it exists
        )
        return vector_store

    def _init_milvus_database(self):
        from pymilvus import MilvusException, connections, db

        # 1. 建立連線
        conn = connections.connect(host="127.0.0.1", port=19530)

        db_name = "milvus_demo"
        try:
            existing_databases = db.list_database()

            # 2. 只在資料庫不存在時才建立，若存在則直接略過刪除動作
            if db_name not in existing_databases:
                db.create_database(db_name)
                print(f"Database '{db_name}' created successfully.")
            else:
                print(f"Database '{db_name}' already exists. Skipping initialization.")

        except MilvusException as e:
            print(f"An error occurred: {e}")

    def _get_llm(self, provider: str):
        return init_chat_model(model=provider, temperature=0)

    def model_config(self, provider: str) -> RunnableConfig:
        if not provider:
            raise ValueError("Please select a model provider for the LLM model.")
        return RunnableConfig(model=provider)

    async def embed(self, collection: str, docs: list[Document]):
        vector_store = self.get_vector_store(collection)
        batch_size = 30
        max_retries = 3
        cooldown = 0.5
        total_splits = len(docs)

        print(f"開始寫入 {total_splits} 個文本切片 (每批 {batch_size} 筆)...")

        # 1. 批次切分迴圈，避免一次性拋送大量請求導致 Ollama 崩潰
        for i in range(0, total_splits, batch_size):
            batch = docs[i : i + batch_size]
            current_range = (
                f"{i + 1}-{min(i + batch_size, total_splits)}/{total_splits}"
            )

            # 2. 自動重試機制
            for attempt in range(1, max_retries + 1):
                try:
                    await vector_store.aadd_documents(batch)
                    print(f"成功寫入批次 [{current_range}]")
                    break
                except Exception as e:
                    print(
                        f"寫入批次 [{current_range}] 失敗 (第 {attempt}/{max_retries} 次嘗試): {e}"
                    )
                    if attempt == max_retries:
                        print(f"批次 [{current_range}] 已達最大重試次數，拋出異常。")
                        raise e

                    # 指數級退讓等待，給 Ollama 內部進程恢復或清理記憶體的時間
                    wait_time = attempt * 2
                    print(f"等待 {wait_time} 秒後重新嘗試...")
                    await asyncio.sleep(wait_time)

            # 3. 每批次成功後短暫停頓，保護 GPU / 記憶體資源
            if cooldown > 0:
                await asyncio.sleep(cooldown)

    async def search(self, query: str, collection: str):
        vector_store = self.get_vector_store(collection)
        return await vector_store.asimilarity_search_with_score(query, k=4)

    async def chat(self, prompt: str, collection: str, provider: str):
        try:
            retriever = self.get_vector_store(collection).as_retriever(
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

            response = await agent.ainvoke({"messages": [("user", prompt)]})

            return response

        except Exception as e:
            print(f"Error during chat: {e}")
            raise

    def embed_query(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)
