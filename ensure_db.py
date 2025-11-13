from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float, text
import os

DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("RENDER_DATABASE_URL") or "sqlite:///app.db"

# create engine (SQLAlchemy will handle postgres/sqlite)
engine = create_engine(DATABASE_URL, echo=False)

metadata = MetaData()

users = Table(
    "users", metadata,
    Column("username", String, primary_key=True),
    Column("algorithm", String, nullable=False),
    Column("iterations", Integer, nullable=False),
    Column("salt", String, nullable=False),
    Column("hash", String, nullable=False),
    Column("role", String, nullable=False, server_default="user"),
    Column("failed_attempts", Integer, nullable=False, server_default="0"),
    Column("last_failed_at", Float, nullable=False, server_default="0")
)

def init_db():
    """
    Ensure database and tables exist. Safe to call on app start.
    If DATABASE_URL points to a managed DB (Render), SQLAlchemy will connect to it.
    """
    metadata.create_all(engine)

def get_engine():
    return engine

if __name__ == "__main__":
    init_db()
    print("DB initialized with engine:", engine)
