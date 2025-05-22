import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Este é o objeto de configuração do Alembic
config = context.config

# Configura logs se o ini estiver presente
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Substitui URL via variável de ambiente (ex: DATABASE_URL do Render)
database_url = os.getenv("DATABASE_URL", "sqlite:///local.db")
config.set_main_option("sqlalchemy.url", database_url)

# ✅ Importa a instância do SQLAlchemy e os modelos
from app import db
target_metadata = db.metadata


def run_migrations_offline():
    """Executa migrações em modo offline."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Executa migrações em modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
