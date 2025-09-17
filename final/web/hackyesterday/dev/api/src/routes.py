import os
from uuid import uuid4
from base64 import b64decode
from threading import Thread
import logging

import magic
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Annotated

from sqlalchemy.orm import Session

from src.authentication import get_current_user, create_access_token
from src.models import (
    get_db,
    UserCreate, UserLogin, UserLeaderboard, UserProfile,
    UserPublicProfile, EditUser,
    ChallengeResponse, ChallengeCreate, SolveChallenge,
    User, Challenge, Solve
)
from src.bot import login_and_view_challenges
from src.utils import get_users_score


api = APIRouter()

MAX_FILE_SIZE = 1024 * 1024 * 3 # 3MB
UPLOADS_DIR = os.getenv("UPLOADS_DIR", "/tmp/")
ALLOWED_FILETYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "pdf": "application/pdf"
}


@api.post('/register')
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken.")

    db_user = User(username=user.username, password=user.password, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"access_token": create_access_token(db_user.id, db_user.is_admin)}

@api.post('/login')
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
    return {"access_token": create_access_token(db_user.id, db_user.is_admin)}

@api.get('/profile/me', response_model=UserProfile)
async def my_profile(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return current_user

@api.get('/profile/is_admin')
async def is_admin(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not admin.")
    return {"message": "You are admin."}

@api.put('/profile/me', response_model=UserProfile)
async def edit_profile(
    edit_user: EditUser,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)):

    tmp_user = db.query(User).filter(User.username == edit_user.username).first()
    if tmp_user and tmp_user.id != current_user.id:
        raise HTTPException(status_code=400, detail="Username already taken.")

    if len(edit_user.password) < 3:
        raise HTTPException(status_code=400, detail="Password must be at least 3 characters long.")

    current_user.username = edit_user.username
    current_user.password = edit_user.password
    db.commit()
    return current_user

@api.get('/profile/{user_id}', response_model=UserPublicProfile)
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@api.get('/challenges', response_model=List[ChallengeResponse])
async def get_challenges(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    if current_user.is_admin:
        challenges = db.query(Challenge).all()
    else:
        challenges = db.query(Challenge).filter(Challenge.draft == False).all()

    for challenge in challenges:
        challenge.solved = challenge.is_solved_by(current_user.id)
    return challenges

@api.get('/challenges/{challenge_id}', response_model=ChallengeResponse)
async def get_challenge(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found.")
    return challenge

@api.post('/challenges/{challenge_id}/solve')
async def solve_challenge(
    challenge_id: int,
    solve: SolveChallenge,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)):

    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found.")

    if challenge.draft:
        raise HTTPException(status_code=403, detail="Challenge is not available.")

    if challenge.flag == solve.flag:
        solve = Solve(user_id=current_user.id, challenge_id=challenge_id)
        db.add(solve)
        db.commit()
        return {"message": "Challenge solved successfully."}

    raise HTTPException(status_code=401, detail='Incorrect flag.')

@api.post('/challenges')
async def create_challenge(
    challenge: ChallengeCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)):

    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not authorized to create challenges.")

    if challenge.score < 0:
        raise HTTPException(status_code=400, detail="Score must be positive.")

    if len(challenge.title) < 3 or len(challenge.description) < 3 or len(challenge.flag) < 3:
        raise HTTPException(status_code=400, detail="Title, description and flag must be at least 3 characters long.")

    if not challenge.attachment_content or not challenge.attachment_filename:
        db_challenge = Challenge(
            title=challenge.title,
            description=challenge.description,
            score=challenge.score,
            flag=challenge.flag
        )
        db.add(db_challenge)
        db.commit()
        return {"message": "Challenge created successfully."}

    file_content = b64decode(challenge.attachment_content)
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Attachment too big.")

    file_extension = challenge.attachment_filename.split(".")[-1].lower()
    file_mimetype = magic.from_buffer(file_content, mime=True)
    if file_extension not in ALLOWED_FILETYPES:
        raise HTTPException(status_code=400, detail="Invalid attachment extension.")

    if file_mimetype != ALLOWED_FILETYPES[file_extension]:
        raise HTTPException(status_code=400, detail="Invalid attachment mimetype.")

    if file_extension == "pdf":
        file_name = os.path.join("pdf", uuid4().hex + "." + file_extension)
    else:
        file_name = os.path.join("images", uuid4().hex + "." + file_extension)

    file_path = os.path.join(UPLOADS_DIR, file_name)
    with open(file_path, "wb") as attachment_file:
        attachment_file.write(file_content)

    db_challenge = Challenge(
        title=challenge.title,
        description=challenge.description,
        score=challenge.score,
        flag=challenge.flag,
        attachment_filename=os.path.join("uploads", file_name),
    )
    db.add(db_challenge)
    db.commit()
    return {"message": "Challenge created successfully."}

@api.get('/leaderboard', response_model=List[UserLeaderboard])
async def leaderboard(db: Session = Depends(get_db)):
    users_score = get_users_score(db)

    users = []
    for user, score in users_score:
        user.score = score
        users.append(user)
    
    return users

@api.get('/prizes')
async def prizes(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)):

    users_score = get_users_score(db)
    if users_score and users_score[0][0].id == current_user.id:
        return {"message": "Congratulations you are the winner of HackYesterday 2025."}

    raise HTTPException(status_code=403, detail="You are not eligible for prizes.")

@api.get('/report')
async def report(current_user: Annotated[User, Depends(get_current_user)]):
    Thread(target=login_and_view_challenges).start()
    logging.info(f"Bot reported by {current_user.username}")
    return {"message": "Bot reported. Please wait..."}