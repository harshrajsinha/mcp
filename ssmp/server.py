from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import uuid
import json

app = FastAPI()

# Connect to Redis
redis_client = redis.Redis(host="103.178.248.133", port=60230, db=0, decode_responses=True)

class SessionRequest(BaseModel):
    client_id: str

@app.post("/session")
async def create_or_get_session(request: SessionRequest):
    """Create or retrieve a session for a client using Redis."""

    client_id = request.client_id
    session_id = redis_client.get(client_id)

    if not session_id:
        session_id = str(uuid.uuid4())  # Generate new session
        redis_client.set(client_id, session_id)
        redis_client.set(session_id, json.dumps([]))

    print(f"Session ID for client {client_id}: {session_id}")

    return {"session_id": session_id}

class QueryRequest(BaseModel):
    session_id: str
    query: str

@app.post("/query")
async def process_query(request: QueryRequest):
    """Process query while managing session data in Redis."""

    session_id = request.session_id

    print(f"Processing query for session ID: {session_id}")

    if not redis_client.exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    # Retrieve context (if stored)
    context_data = redis_client.get(session_id)
    context = json.loads(context_data) if context_data else []

    # Mock response using session tracking
    response = {
        "answer": f"Processed query: '{request.query}' using session ID {session_id}",
        "session_id": session_id,
        "context": context
    }

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(response)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # Store updated context (for continuity)
    response["context"].append({"role": "user", "content": request.query})
    redis_client.set(session_id, json.dumps(response["context"]))

    return response
