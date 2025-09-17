import os
from datetime import datetime, timedelta
import random
import secrets

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Create a SQLite database
engine = create_engine('sqlite:///challenge.db',
    pool_size=10, max_overflow=20, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Get a database connection instance"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_data():
    """Add users and challenges to the database"""
    db = SessionLocal()

    if db.query(Challenge).count() == 0:
        db_challenges = [
            Challenge(title="Cryptography", description="17+8?", score=20, draft=False, flag="hackyesterday{yeah}"),
            Challenge(title="Reverse Engineering", description="bpi atnic uka", score=30, draft=False, flag="hackyesterday{pembohong}"),
            Challenge(title="Pwn", description="Siapa fans Linz disini?", score=50, draft=False, flag="hackyesterday{aku_bang}"),
        ]
        db.add_all(db_challenges)
        db.commit()

    if db.query(User).count() == 0:
        db_users = []
        for username in ["jokowo", "ganjal", "gibram", "prabomo", "bahlir", "kuch nafari", "arif satria", "when yh menang :("]:
            db_users.append(User(username=username, password=secrets.token_hex(),
                last_solve=datetime.now() - timedelta(days=random.randint(1, 30))
            ))

        random_user = random.choice(db_users)
        random_user.is_admin = True
        random_user.password = os.getenv("FLAG", "FLAG not set.")

        db.add_all(db_users)
        db.commit()

    if db.query(Solve).count() == 0:
        db_solves = []
        for user_id in range(1, 7):
            for challenge_id in range(1, random.randint(2, 4)):
                db_solves.append(Solve(user_id=user_id, challenge_id=challenge_id))

        db_solves.extend([
            Solve(user_id=8, challenge_id=1),
            Solve(user_id=8, challenge_id=2),
            Solve(user_id=8, challenge_id=3)
        ])

        db.add_all(db_solves)
        db.commit()

    db.close()


class User(Base):
    """User model in database"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    last_solve = Column(DateTime, default=datetime.now())

class Challenge(Base):
    """Challenge model in database"""
    __tablename__ = 'challenges'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    score = Column(Integer)
    draft = Column(Boolean, default=True)
    flag = Column(String)
    attachment_filename = Column(String, default="")

    def is_solved_by(self, user_id):
        db = SessionLocal()
        return db.query(Solve).filter_by(user_id=user_id, challenge_id=self.id).first() is not None

class Solve(Base):
    """Solve model in database"""
    __tablename__ = 'solves'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    challenge_id = Column(Integer, ForeignKey('challenges.id'))
    solve_date = Column(DateTime, default=datetime.now())


Base.metadata.create_all(bind=engine)
init_data()

class ChallengeCreate(BaseModel):
    title: str
    description: str
    score: int
    flag: str
    attachment_filename: str
    attachment_content: str

class ChallengeResponse(BaseModel):
    id: int
    title: str
    description: str
    score: int
    draft: bool
    attachment_filename: str
    solved: bool

class SolveChallenge(BaseModel):
    flag: str

class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False

class UserLeaderboard(BaseModel):
    username: str
    score: int
    last_solve: datetime

class UserLogin(BaseModel):
    username: str
    password: str

class EditUser(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    id: int
    username: str
    password: str
    is_admin: bool
    last_solve: datetime

class UserPublicProfile(BaseModel):
    id: int
    username: str
    is_admin: bool
