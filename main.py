import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents, db

app = FastAPI(title="Fitness App API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request bodies (thin wrappers around schemas)
class ExerciseIn(BaseModel):
    name: str
    sets: int
    reps: int

class WorkoutIn(BaseModel):
    title: str
    difficulty: Optional[str] = "Beginner"
    exercises: List[ExerciseIn] = []

class LogIn(BaseModel):
    date: str
    workout_title: str
    notes: Optional[str] = None
    duration_minutes: Optional[int] = None

@app.get("/")
def read_root():
    return {"message": "Fitness App Backend is running"}

# Public sample workouts endpoint
@app.get("/api/workouts")
def list_workouts():
    try:
        items = get_documents("workout", limit=50)
        # Convert ObjectId to string if present
        for it in items:
            if "_id" in it:
                it["id"] = str(it.pop("_id"))
        return {"items": items}
    except Exception:
        # Fallback: return a few curated workouts if DB not available
        sample = [
            {
                "id": "w1",
                "title": "Full Body Starter",
                "difficulty": "Beginner",
                "exercises": [
                    {"name": "Bodyweight Squats", "sets": 3, "reps": 12},
                    {"name": "Push Ups", "sets": 3, "reps": 10},
                    {"name": "Plank (sec)", "sets": 3, "reps": 30},
                ],
            },
            {
                "id": "w2",
                "title": "Upper Body Blast",
                "difficulty": "Intermediate",
                "exercises": [
                    {"name": "Pull Ups", "sets": 4, "reps": 6},
                    {"name": "Dumbbell Press", "sets": 4, "reps": 10},
                    {"name": "Rows", "sets": 4, "reps": 10},
                ],
            },
        ]
        return {"items": sample}

@app.post("/api/workouts")
def create_workout(workout: WorkoutIn):
    try:
        inserted = create_document("workout", workout.model_dump())
        return {"id": inserted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs")
def list_logs():
    try:
        items = get_documents("log", limit=100)
        for it in items:
            if "_id" in it:
                it["id"] = str(it.pop("_id"))
        return {"items": items}
    except Exception:
        return {"items": []}

@app.post("/api/logs")
def create_log(log: LogIn):
    try:
        inserted = create_document("log", log.model_dump())
        return {"id": inserted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
