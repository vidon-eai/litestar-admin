class AppException(Exception):
    """應用層業務異常基類"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class UserNotFoundException(AppException):
    def __init__(self, message: str = "User not found"):
        super().__init__(message=message, status_code=404)


class PermissionDeniedException(AppException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message=message, status_code=403)


class ServiceException(Exception):
    """通用服務異常，例如衝突或狀態不允許"""

    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)
