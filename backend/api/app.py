from fastapi import FastAPI, File, UploadFile
import shutil
import os
from backend.model.extract_text import extract_text

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):
    """Uploads a resume file, extracts text, and returns it."""
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the file temporarily
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    extracted_text = extract_text(file_path)

    # Delete file after processing
    os.remove(file_path)

    if extracted_text:
        return {"filename": file.filename, "extracted_text": extracted_text}
    else:
        return {"error": "Failed to extract text"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)