# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import SessionLocal, Word

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Dictionary Chatbot API!"}

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # ✅ Create a new word
# @app.post("/words/")
# def create_word(word: str, definition: str, db: Session = Depends(get_db)):
#     db_word = Word(word=word, definition=definition)
#     db.add(db_word)
#     db.commit()
#     db.refresh(db_word)
#     return db_word

# # ✅ Get a word's definition
# @app.get("/words/{word}")
# def get_word(word: str, db: Session = Depends(get_db)):
#     db_word = db.query(Word).filter(Word.word == word).first()
#     if not db_word:
#         raise HTTPException(status_code=404, detail="Word not found")
#     return db_word

# # ✅ Update a word's definition
# @app.put("/words/{word}")
# def update_word(word: str, definition: str, db: Session = Depends(get_db)):
#     db_word = db.query(Word).filter(Word.word == word).first()
#     if not db_word:
#         raise HTTPException(status_code=404, detail="Word not found")
#     db_word.definition = definition
#     db.commit()
#     return db_word

# # ✅ Delete a word
# @app.delete("/words/{word}")
# def delete_word(word: str, db: Session = Depends(get_db)):
#     db_word = db.query(Word).filter(Word.word == word).first()
#     if not db_word:
#         raise HTTPException(status_code=404, detail="Word not found")
#     db.delete(db_word)
#     db.commit()
#     return {"message": f"Word '{word}' deleted successfully"}


# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # 1️⃣ Fetch a word definition
# @app.get("/api/dictionary/{word}")
# def get_word(word: str, db: Session = Depends(get_db)):
#     db_word = db.query(Word).filter(Word.word == word).first()
#     if not db_word:
#         raise HTTPException(status_code=404, detail="Word not found")
#     return db_word

# # 2️⃣ Add a new word
# @app.post("/api/dictionary")
# def add_word(word: str, definition: str, synonyms: str = None, antonyms: str = None, added_by: str = "admin", db: Session = Depends(get_db)):
#     db_word = Word(word=word, definition=definition, synonyms=synonyms, antonyms=antonyms, added_by=added_by)
#     db.add(db_word)
#     db.commit()
#     db.refresh(db_word)
#     return {"message": "Word added successfully", "word": db_word.word}

# # 3️⃣ Update an existing word
# @app.put("/api/dictionary/{word}")
# def update_word(word: str, definition: str, synonyms: str = None, antonyms: str = None, db: Session = Depends(get_db)):
#     db_word = db.query(Word).filter(Word.word == word).first()
#     if not db_word:
#         raise HTTPException(status_code=404, detail="Word not found")
#     db_word.definition = definition
#     db_word.synonyms = synonyms
#     db_word.antonyms = antonyms
#     db.commit()
#     return {"message": "Word updated successfully"}

# # 4️⃣ Delete a word
# @app.delete("/api/dictionary/{word}")
# def delete_word(word: str, db: Session = Depends(get_db)):
#     db_word = db.query(Word).filter(Word.word == word).first()
#     if not db_word:
#         raise HTTPException(status_code=404, detail="Word not found")
#     db.delete(db_word)
#     db.commit()
#     return {"message": "Word deleted successfully"}

# # 5️⃣ Autocomplete Suggestions
# @app.get("/api/dictionary/suggest")
# def suggest_words(query: str, db: Session = Depends(get_db)):
#     words = db.query(Word.word).filter(Word.word.like(f"{query}%")).limit(5).all()
#     return {"suggestions": [word[0] for word in words]}




from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
from database import SessionLocal, Word
from pydantic import BaseModel
from fastapi.responses import JSONResponse 
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token, get_current_user
from datetime import timedelta

from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "custom_message": "Something went wrong!"},
    )

fake_db = {"hello": "A greeting", "python": "A programming language"}

class WordRequest(BaseModel):
    word: str
    meaning: str

@app.post("/add-word/")
def add_word(word_data: WordRequest):
    if len(word_data.word) < 2:
        raise HTTPException(status_code=422, detail="Word must be at least 2 characters long.")
    return {"message": f"Added word: {word_data.word}"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Protected Route (Only Authenticated Users)
@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"username": current_user["username"], "email": current_user["email"]}


@app.get("/")
def read_root():
    return {"message": "Welcome to the Dictionary AI Chatbot API!"}
# Dependency to get DB session and close it after use

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Create a new word
@app.post("/words/")
def create_word(word: str, definition: str, db: Session = Depends(get_db)):
    db_word = Word(word=word, definition=definition)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word

# ✅ Get a word's definition
@app.get("/words/{word}")
def get_word(word: str, db: Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.word == word).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word not found")
    return db_word

# ✅ Update a word's definition
@app.put("/words/{word}")
def update_word(word: str, definition: str, db: Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.word == word).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word not found")
    db_word.definition = definition
    db.commit()
    return db_word

# ✅ Delete a word
@app.delete("/words/{word}")
def delete_word(word: str, db: Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.word == word).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Word not found")
    db.delete(db_word)
    db.commit()
    return {"message": f"Word '{word}' deleted successfully"}
