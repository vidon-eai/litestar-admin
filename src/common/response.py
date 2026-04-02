# schemas.py
from datetime import datetime
from typing import Any, Optional, Generic
from pydantic import BaseModel, Field
from pydantic.types import T


class UnifiedResponse(BaseModel, Generic[T]):
    code: int = Field(description="Business status code")
    data: Optional[T] = Field(default=None, description="Return data")
    status_code: int = Field(description="HTTP status code")
    is_success: bool = Field(description="Whether the request is successful")
    msg: str = Field(description="Response message")
    timestamp: str = Field(description="Response time")

    class Config:
        # 允许在模型中使用 datetime 等对象，稍后在序列化时处理
        json_encoders = {datetime: lambda v: v.isoformat()}

    @classmethod
    def success(
        cls,
        data: Optional[T] = None,
        msg: str = "Success",
        code: int = 200,
        status_code: int = 200,
    ) -> "UnifiedResponse[T]":
        return cls(
            code=code,
            data=data,
            status_code=status_code,
            is_success=True,
            msg=msg,
            timestamp=datetime.now().isoformat(),
        )

    @classmethod
    def error(
        cls,
        msg: str = "Failed",
        code: int = 500,
        status_code: int = 500,
        data: Optional[T] = None,
    ) -> "UnifiedResponse[T]":
        return cls(
            code=code,
            data=data,
            status_code=status_code,
            is_success=False,
            msg=msg,
            timestamp=datetime.now().isoformat(),
        )
