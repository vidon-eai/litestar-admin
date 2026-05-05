from enum import Enum
from advanced_alchemy.extensions.litestar import providers
from litestar import Controller, post
from app.common.response import COMMON_RESPONSES, ResponseSchema, SuccessResponse
from app.modules.system.post.schema import PostCreate, PostRead
from app.modules.system.post.service import PostService


# 定义模型字段枚举
class PostSortField(str, Enum):
    TITLE = "title"
    CONTENT = "content"


class PostController(Controller):
    path = "/posts"
    tags = ["Post Management"]

    dependencies = {
        **providers.create_service_dependencies(
            PostService,
            "post_service",
        )
    }

    @post("/", responses={**COMMON_RESPONSES})
    async def create_post(
        self, post_service: PostService, data: PostCreate
    ) -> ResponseSchema[PostRead]:
        result = await post_service.create(data)

        return SuccessResponse(
            data=post_service.to_schema(result, schema_type=PostRead),
            detail="Post創建成功",
        )
