from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

from .service import RAGService

if TYPE_CHECKING:
    from litestar import Litestar
    from litestar.datastructures.state import State


@dataclass
class RAGConfig:
    dependency_key: str = "rag_service"
    app_state_key: str = "rag_service"

    llm_model: str = "qwen2.5:7b"
    embedding_model: str = "qwen3-embedding:8b"

    def create_service(self) -> RAGService:
        return RAGService(self)

    def create_app_state_items(self) -> dict[str, Any]:
        return {
            self.app_state_key: self.create_service(),
        }

    def update_app_state(self, app: "Litestar") -> None:
        app.state.update(self.create_app_state_items())

    @asynccontextmanager
    async def lifespan(self, app: "Litestar") -> AsyncGenerator[None, None]:
        deps = self.create_app_state_items()
        app.state.update(deps)
        try:
            yield
        finally:
            pass

    def provide_service(self, state: "State") -> RAGService:
        return cast(RAGService, state.get(self.app_state_key))
