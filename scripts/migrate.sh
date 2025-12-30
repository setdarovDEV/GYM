#!/bin/bash

mkdir -p migrations/versions

if [ ! -f "migrations/alembic.ini" ]; then
    alembic init migrations
    sed -i "s|sqlalchemy.url = .*|sqlalchemy.url = ${DATABASE_URL:-postgresql+asyncpg://postgres:postgres@localhost:5432/gym_delivery}|" migrations/alembic.ini
    sed -i "s|# from myapp import mymodel|from src.core.database import Base|" migrations/env.py
    sed -i "s|target_metadata = None|target_metadata = Base.metadata|" migrations/env.py
fi

alembic revision --autogenerate -m "$1"

alembic upgrade head