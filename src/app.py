from flask import Flask

from src.config.settings import settings
from src.config.database import SessionLocal, Base, engine

from src.shared.exceptions.handlers import register_error_handlers
from src.shared.middlewares.request_logger import register_request_logger

from src.modules.users.interfaces.routes import users_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["DEBUG"] = settings.DEBUG

    # --- Blueprints (rutas por módulo) ---
    register_blueprints(app)

    # --- Error handlers globales ---
    register_error_handlers(app)

    # --- Middlewares (logging de requests, etc.) ---
    register_request_logger(app)

    # --- Ciclo de vida de la sesión de BD (scoped_session) ---
    @app.teardown_appcontext
    def remove_session(exception=None):
        SessionLocal.remove()

    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(users_bp)
    # app.register_blueprint(orders_bp)  # futuros módulos van aquí