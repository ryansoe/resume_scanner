from fastapi import FastAPI, File, UploadFile
import shutil
import os
from backend.model.extract_text import extract_text
from backend.api.database import get_db_connection

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):
    """Uploads a resume file, extracts text, stores it in PostgreSQL, and returns the response."""
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file temporarily
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    extracted_text = extract_text(file_path)
    os.remove(file_path)

    if extracted_text:
        # Store in database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO resumes (filename, extracted_text) VALUES (%s, %s) RETURNING id",
                (file.filename, extracted_text),
            )
            resume_id = cursor.fetchone()["id"]
            conn.commit()
            cursor.close()
            conn.close()
            return {"resume_id": resume_id, "filename": file.filename, "extracted_text": extracted_text}
        else:
            return {"error": "Database connection failed"}
    else:
        return {"error": "Failed to extract text"}
    
@app.get("/resumes/")
async def get_resumes():
    """Fetch all stored resumes from PostgreSQL."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename, extracted_text, uploaded_at FROM resumes ORDER BY uploaded_at DESC")
        resumes = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"resumes": resumes}
    else:
        return {"error": "Database connection failed"}