# src/shared/auth/decorators.py
from functools import wraps
from flask import request, g
from src.shared.auth.jwt_provider import AuthProvider
from src.shared.exceptions.base import UnauthorizedException, ForbiddenException

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from src.config.container import container  # import diferido, evita import circular

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise UnauthorizedException()

        token = auth_header.split(" ", 1)[1].strip()

        strategy = container.auth_strategy
        payload = strategy.validate_token(token)

        g.current_user_id = payload["sub"]
        g.current_user_correo = payload.get("correo")

        return func(*args, **kwargs)
    return wrapper

def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_role = getattr(request, "user", {}).get("role")
            if user_role not in roles:
                raise ForbiddenException("No tienes permisos para este recurso")
            return f(*args, **kwargs)
        return wrapper
    return decorator