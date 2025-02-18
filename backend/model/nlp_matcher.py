import torch
from sentence_transformers import SentenceTransformer, util
from backend.api.database import get_db_connection

# Load a pre-trained NLP model (BERT-based embeddings)
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def compute_similarity(resume_text, job_description):
    """Compute similarity score between a resume and a job description."""
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    similarity_score = util.pytorch_cos_sim(resume_embedding, job_embedding)
    return similarity_score.item()  # Convert tensor to a scalar value

def find_best_resumes(job_description, top_n=5):
    """Fetch resumes from the database and rank them based on job relevance."""
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}

    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, extracted_text FROM resumes")
    resumes = cursor.fetchall()
    cursor.close()
    conn.close()

    if not resumes:
        return {"error": "No resumes found in the database"}

    # Compute similarity for each resume
    scored_resumes = [
        {"id": r["id"], "filename": r["filename"], "score": compute_similarity(r["extracted_text"], job_description)}
        for r in resumes
    ]

    # Sort by highest similarity score
    ranked_resumes = sorted(scored_resumes, key=lambda x: x["score"], reverse=True)

    return ranked_resumes[:top_n]