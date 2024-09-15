from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Document, User
from app.schemas import SearchQuery, UserRequest
from app.utils import encode_text, cosine_similarity, check_rate_limit
from app.cache import get_from_cache, set_to_cache
import time

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "API is active"}

@app.post("/search")
async def search(query: SearchQuery, user: UserRequest, db: Session = Depends(get_db)):
    # Rate limiting
    check_rate_limit(db, user.user_id)

    # Cache lookup
    cache_key = f"{user.user_id}:{query.text}:{query.top_k}"
    cached_results = get_from_cache(cache_key)
    if cached_results:
        return {"results": cached_results}

    # Start inference time
    start_time = time.time()

    # Query database for documents
    documents = db.query(Document).all()
    results = []
    query_embedding = encode_text(query.text)

    for doc in documents:
        doc_embedding = encode_text(doc.content)
        similarity = cosine_similarity(query_embedding,
