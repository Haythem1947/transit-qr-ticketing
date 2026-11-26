"""Run: python check_db.py  -> shows if the app can reach MySQL and which tables exist."""
from sqlalchemy import inspect

from app.db import engine, init_db

init_db()
print("Connected to:", engine.url.render_as_string(hide_password=True))
print("Tables:", inspect(engine).get_table_names())
