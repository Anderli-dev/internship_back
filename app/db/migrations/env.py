import asyncio
import os
from logging.config import fileConfig
from app.core.settings import logger

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

from app.db.models import *
from app.db.base import BaseModel

# Load environment variables
load_dotenv()

# Get Alembic configuration
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Retrieve the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Replace with localhost since migrations are performed locally
# DATABASE_URL = DATABASE_URL.replace("postgres:", "localhost:")

# Set the database URL in the Alembic configuration
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Set metadata for Alembic
target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (without connecting to the database)."""
    logger.info(f"Runing offline migrations.")
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode (with a database connection)."""
    logger.info(f"Runing online migrations.")
    engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()


def do_run_migrations(connection):
    """Execute migrations in synchronous mode within an asynchronous connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
