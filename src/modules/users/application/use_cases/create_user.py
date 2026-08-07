from src.modules.users.domain.entities import UserEntity
from src.modules.users.domain.repositories import UserRepository
from src.modules.users.domain.exceptions import UserAlreadyExistsException
from src.modules.users.application.dto import CreateUserDTO, UserResponseDTO
from src.shared.auth.password_hasher import PasswordHasher  # lo definimos si no existe aún


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher, session):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.session = session

    def execute(self, dto: CreateUserDTO) -> UserResponseDTO:
        if self.user_repository.get_by_correo(dto.correo):
            raise UserAlreadyExistsException(dto.correo)

        if self.user_repository.get_by_nick(dto.nick):
            raise UserAlreadyExistsException(dto.nick)

        hashed_password = self.password_hasher.hash(dto.password)

        user = UserEntity(
            nombre=dto.nombre,
            apellido=dto.apellido,
            correo=dto.correo,
            nick=dto.nick,
            password=hashed_password,
            id_usuario_creador=dto.id_usuario_creador,
        )
        try:
            created_user = self.user_repository.create(user)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise
        return UserResponseDTO.from_entity(created_user)