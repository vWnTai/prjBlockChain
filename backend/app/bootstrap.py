import os
from alembic import command
from alembic.config import Config
from pwdlib import PasswordHash
from sqlalchemy import select
from app.db import Session
from app.models import User


def main():
    command.upgrade(Config("alembic.ini"), "head")
    with Session.begin() as db:
        for username, role in [("admin", "Admin"), ("analyst", "Analyst"), ("viewer", "Viewer")]:
            if db.scalar(select(User).where(User.username == username)) is None:
                password = os.environ[username.upper() + "_PASSWORD"]
                if len(password) < 16:
                    raise ValueError("Local account passwords must have at least 16 characters")
                db.add(
                    User(
                        username=username, role=role, password_hash=PasswordHash.recommended().hash(password)
                    )
                )
    print("Migration and local account bootstrap completed.")


if __name__ == "__main__":
    main()
