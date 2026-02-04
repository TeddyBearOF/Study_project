from typing import Optional


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int,
        details: Optional[dict] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class EntityNotFoundException(AppException):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(
            message=f"{entity_name} с ID {entity_id} не найден",
            status_code=404
        )


class EntityAlreadyExistsException(AppException):
    def __init__(self, entity_name: str, field: str, value: str):
        super().__init__(
            message=f"{entity_name} с {field}={value} уже существует",
            status_code=400
        )


class InvalidInputDataException(AppException):
    def __init__(self, reason: str):
        super().__init__(
            message="Некорректные входные данные",
            status_code=422,
            details={"reason": reason}
        )


class UnauthorizedException(AppException):
    def __init__(self):
        super().__init__(
            message="Доступ запрещён: требуется авторизация",
            status_code=401
        )


class ForbiddenException(AppException):
    def __init__(self):
        super().__init__(
            message="Недостаточно прав для выполнения действия",
            status_code=403
        )


class InternalServerException(AppException):
    def __init__(self, details: str = "Неизвестная ошибка"):
        super().__init__(
            message="Внутренняя ошибка сервера",
            status_code=500,
            details={"error": details}
        )