from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

from src.config.settings import settings

# Engine: maneja el pool de conexiones a Postgres
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # valida conexiones "muertas" antes de usarlas
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG,  # imprime SQL en consola si DEBUG=True
)

# Factory de sesiones
SessionLocal = scoped_session(
    sessionmaker(bind=engine, autocommit=False, autoflush=False)
)

# Base declarativa: todos los modelos (UserModel, etc.) heredan de aquí
Base = declarative_base()