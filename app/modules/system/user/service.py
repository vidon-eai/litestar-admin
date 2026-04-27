from advanced_alchemy.filters import LimitOffset
from advanced_alchemy.service import (
    SQLAlchemyAsyncRepositoryService,
)
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import or_
from app.modules.system.user.model import User

class UserService(SQLAlchemyAsyncRepositoryService[User]):

    class Repo(SQLAlchemyAsyncRepository[User]):
        model_type = User

    repository_type = Repo
    
    
    async def search(self, query: str | None = None, page: int = 1, page_size:int = 10) -> list[User]:
        offset = (page-1) * page_size
        
        if not query:
            return await self.repository.list_and_count(LimitOffset(offset=offset, limit=page_size))
        
        search_term = f"%{query}%"
        conditions = [
            User.username.ilike(search_term),
            User.description.ilike(search_term),
            User.phone.ilike(search_term)
        ]
        
        
        return await self.repository.list_and_count(or_(*conditions), LimitOffset(offset=offset, limit=page_size))