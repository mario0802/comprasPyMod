from src.modules.users.domain.repositories import UserRepository
from src.modules.users.domain.exceptions import UserNotFoundException
from src.modules.users.application.dto import UserResponseDTO


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> UserResponseDTO:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)

        return UserResponseDTO.from_entity(user)