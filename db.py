from ensure_db import engine, users
from sqlalchemy import select, insert, update
from sqlalchemy.exc import NoResultFound

def add_or_update_user(username, algorithm, iterations, salt, hashhex, role="user"):
    stmt = insert(users).values(
        username=username, algorithm=algorithm, iterations=iterations, salt=salt, hash=hashhex, role=role
    ).on_conflict_do_update(
        index_elements=[users.c.username],
        set_={"algorithm": algorithm, "iterations": iterations, "salt": salt, "hash": hashhex, "role": role}
    )
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

def get_user(username):
    stmt = select(users).where(users.c.username == username)
    with engine.connect() as conn:
        r = conn.execute(stmt).mappings().fetchone()
        return dict(r) if r else None

def list_users():
    stmt = select(users.c.username, users.c.role)
    with engine.connect() as conn:
        rows = conn.execute(stmt).mappings().fetchall()
        return [dict(r) for r in rows]
