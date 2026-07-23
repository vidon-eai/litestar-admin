from uuid import UUID

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from app.db.models import Dataset
from sqlalchemy.orm import selectinload


class DatasetService(SQLAlchemyAsyncRepositoryService[Dataset]):
    class Repo(SQLAlchemyAsyncRepository[Dataset]):
        model_type = Dataset

    repository_type = Repo

    async def get_dataset_with_collections(self, dataset_id: UUID) -> Dataset:

        return await self.get(dataset_id, load=[selectinload(Dataset.collections)])
