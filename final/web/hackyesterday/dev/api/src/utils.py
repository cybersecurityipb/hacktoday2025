import time
import threading
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from contextlib import asynccontextmanager

from src.models import User, Challenge, Solve, SessionLocal

stop_event = threading.Event()

def get_users_score(db: Session):
    return (
        db.query(User, func.sum(Challenge.score).label("total_score"))
        .join(Solve, Solve.challenge_id == Challenge.id)
        .join(User, Solve.user_id == User.id)
        .group_by(User.id)
        .order_by(desc("total_score"), User.last_solve.asc())
        .all()
    )

def draft_challenge_remover():
    while not stop_event.is_set():
        db = SessionLocal()
        try:
            drafted = db.query(Challenge).filter(Challenge.draft == True).all()
            if drafted:
                for challenge in drafted:
                    db.delete(challenge)
                db.commit()
        except Exception as e:
            db.rollback()
        finally:
            db.close()

        stop_event.wait(60)

@asynccontextmanager
async def lifespan(app):
    thread = threading.Thread(target=draft_challenge_remover, daemon=True)
    thread.start()

    yield

    stop_event.set()
    thread.join()
