from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

from .service import StorageService

if TYPE_CHECKING:
    from litestar import Litestar
    from litestar.datastructures.state import State

@dataclass
class StorageConfig:
    root_path: str = "./storage"
    storage_dependency_key: str = "storage_service"
    storage_app_state_key: str = "storage_service"

    def create_storage_service(self) -> StorageService:
        return StorageService(self)

    def create_app_state_items(self) -> dict[str, Any]:
        return {
            self.storage_app_state_key: self.create_storage_service(),
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

    def provide_storage(self, state: "State") -> StorageService:
        return cast(StorageService, state.get(self.storage_app_state_key))