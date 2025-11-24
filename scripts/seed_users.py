#!/usr/bin/env python3
"""Seed script to create admin/teacher/student test users.

Usage:
  python scripts/seed_users.py

This script uses the project's `src` package (SQLAlchemy + auth helpers).
"""
from src.db import SessionLocal
from src.auth import create_db_and_tables, UserDB, get_password_hash


def seed_users():
    create_db_and_tables()
    db = SessionLocal()
    users = [
        {"email": "admin@school.edu", "full_name": "Site Admin", "password": "adminpass", "role": "admin"},
        {"email": "teacher@school.edu", "full_name": "Lead Teacher", "password": "teacherpass", "role": "teacher"},
        {"email": "student@school.edu", "full_name": "Test Student", "password": "studentpass", "role": "student"},
    ]

    created = []
    try:
        for u in users:
            existing = db.query(UserDB).filter(UserDB.email == u["email"]).first()
            if existing:
                print(f"User {u['email']} already exists (role={existing.role})")
                created.append(existing.email)
                continue

            user = UserDB(
                email=u["email"],
                full_name=u.get("full_name"),
                hashed_password=get_password_hash(u["password"]),
                role=u.get("role", "student"),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            created.append(user.email)
            print(f"Created user: {user.email} (role={user.role})")
    finally:
        db.close()

    print("Done. Created/confirmed:", created)


if __name__ == "__main__":
    seed_users()
