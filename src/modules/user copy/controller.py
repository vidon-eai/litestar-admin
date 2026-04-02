from litestar import Controller, get, post
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_404_NOT_FOUND
from src.common.response import UnifiedResponse
from src.core.logger import log
from src.core.base_query_params import QueryFilter
from litestar.di import Provide


class UserController(Controller):
    path = "/users"
    tags = ["User management"]

    @get(
        "/",
        summary="Get users",
        description="Retrieve a list of users",
        dependencies={"query_params": Provide(QueryFilter, sync_to_thread=False)},
    )
    async def get_users(self, query_params: QueryFilter) -> QueryFilter:
        log.info("Getting users")
        return query_params

    @get(
        "/{userId:int}",
        summary="Get user by ID",
        description="Retrieve a user by their ID",
    )
    async def get_user_by_id(self, userId: int) -> UnifiedResponse[dict]:
        return UnifiedResponse.success(
            status_code=200,
            msg="User retrieved successfully",
            data={"id": userId, "name": "John Doe"},
        )

    @post(
        "/",
        summary="Create user",
        description="Create a new user",
    )
    async def create_user(self) -> UnifiedResponse[dict]:
        return UnifiedResponse.success(
            status_code=201,
            msg="User created successfully",
            data={"id": 1, "name": "John Doe"},
        )
