from src.shared.auth.strategies.base import AuthStrategy

class AuthProvider:
    _strategy: AuthStrategy = None

    @classmethod
    def init(cls, strategy: AuthStrategy):
        cls._strategy = strategy

    @classmethod
    def get_strategy(cls) -> AuthStrategy:
        if cls._strategy is None:
            raise RuntimeError("AuthProvider no inicializado")
        return cls._strategy