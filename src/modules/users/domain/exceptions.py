from src.shared.exceptions.base import DomainException


class UserAlreadyExistsException(DomainException):
    def __init__(self, correo: str):
        super().__init__(f"Ya existe un usuario con el correo '{correo}'")


class UserNotFoundException(DomainException):
    def __init__(self, user_id: int):
        super().__init__(f"Usuario con id '{user_id}' no encontrado")