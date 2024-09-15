from sentence_transformers import SentenceTransformer
import numpy as np
from fastapi import HTTPException

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def encode_text(text: str):
    return model.encode(text)

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def check_rate_limit(db, user_id):
    user = db.query(User).filter_by(user_id=user_id).first()
    if user and user.api_calls > 5:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    if not user:
        user = User(user_id=user_id, api_calls=1)
        db.add(user)
    else:
        user.api_calls += 1
    db.commit()
