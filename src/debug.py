from sqlmodel import Session
from sqlalchemy import text
from src.db import engine

with Session(engine) as session:
    result = session.exec(
        text(
            "EXPLAIN QUERY PLAN SELECT * FROM roomuser WHERE room_id = 1 AND user_id = 1;"
        )
    )
    for row in result:
        print(row)
