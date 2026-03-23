from fastapi import UploadFile, File
from voice.voice_auth import get_embedding, embedding_to_bytes
from voice.voice_auth import compare_embeddings, bytes_to_embedding

from fastapi import FastAPI, Form, HTTPException
from db import SessionLocal
from auth import authenticate_user, hash_password
from models import User

from fastapi import UploadFile, File
from voice.stt import speech_to_text
from translation.translate import translate_to_english

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for now (dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/voice-command")
async def process_voice(file: UploadFile = File(...)):
    
    # Save file
    file_path = "temp_command.wav"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # STEP 1: STT
    text, language = speech_to_text(file_path)

    # STEP 2: Translation
    translated = translate_to_english(text)

    return {
        "original_text": text,
        "language": language,
        "translated_text": translated,
        "response": "Processed successfully"
    }

@app.post("/signup")
async def signup(
    customer_id: str = Form(...),
    password: str = Form(...),
    file: UploadFile = File(...)
):
    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.customer_id == customer_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Save audio file temporarily
        file_location = f"temp_login_{customer_id}.webm"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Convert to embedding
        embedding = get_embedding(file_location)
        embedding_bytes = embedding_to_bytes(embedding)

        # Hash password
        hashed_password = hash_password(password)

        # Save user
        new_user = User(
            customer_id=customer_id,
            password_hash=hashed_password,
            voice_embedding=embedding_bytes
        )

        db.add(new_user)
        db.commit()

    finally:
        db.close()

    return {"status": "success", "message": "User created"}

@app.post("/login")
async def login(
    customer_id: str = Form(...),
    password: str = Form(...),
    file: UploadFile = File(...)
):
    db = SessionLocal()

    try:
        user = authenticate_user(db, customer_id, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Save login audio
        file_location = f"temp_login_{customer_id}.webm"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Generate embedding
        input_embedding = get_embedding(file_location)

        # Get stored embedding
        stored_embedding = bytes_to_embedding(user.voice_embedding)

        # Compare
        match, score = compare_embeddings(input_embedding, stored_embedding)

        print("Similarity:", score)

        if not match:
            raise HTTPException(status_code=401, detail="Voice authentication failed")

    finally:
        db.close()

    return {"status": "success", "message": "Login successful"}