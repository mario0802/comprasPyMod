from flask import Flask
from flask_smorest import Api

from src.config.settings import settings
from src.config.database import SessionLocal, Base, engine

from src.shared.exceptions.handlers import register_error_handlers
from src.shared.middlewares.request_logger import register_request_logger
from src.shared.auth.jwt_provider import AuthProvider
from src.shared.auth.strategies.jwt_strategy import JWTAuthStrategy

from src.modules.users.interfaces.routes import users_bp
from src.modules.compra.solicitudes_compra.interfaces.routes import solicitudes_compra_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(settings)

    AuthProvider.init(
        JWTAuthStrategy(
            secret_key=settings.JWT_SECRET_KEY,
            expires_in_minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MIN,
        )
    )

    # --- Swagger / OpenAPI ---
    api = Api(app)

    # --- Blueprints (rutas por módulo) ---
    register_blueprints(api)

    # --- Error handlers globales ---
    register_error_handlers(app)

    # --- Middlewares (logging de requests, etc.) ---
    register_request_logger(app)

    # --- Ciclo de vida de la sesión de BD (scoped_session) ---
    @app.teardown_appcontext
    def remove_session(exception=None):
        SessionLocal.remove()

    return app


def register_blueprints(api: Api) -> None:
    api.register_blueprint(users_bp)
    api.register_blueprint(solicitudes_compra_bp)