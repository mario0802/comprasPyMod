import bcrypt

class PasswordHasher:
    """
    Utilidad transversal para hashear y verificar contraseñas usando bcrypt.
    """

    def __init__(self, rounds: int = 12):
        self.rounds = rounds

    def hash(self, plain_password: str) -> str:
        if not plain_password:
            raise ValueError("La contraseña no puede estar vacía")

        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        if not plain_password or not hashed_password:
            return False

        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )