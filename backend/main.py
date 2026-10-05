from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Cartoon Animal Illustrations API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Asset(BaseModel):
    id: int
    title: str
    status: str
    score: float
    timestamp: str
    asset_url: str
    category: str

# In-memory seed data
assets_db = [
    {"id": 1, "title": "Happy Hippo", "status": "approved", "score": 9.5, "timestamp": "2023-10-27T10:00:00Z", "asset_url": "/assets/hippo.png", "category": "mammal"},
    {"id": 2, "title": "Dancing Duck", "status": "pending", "score": 8.2, "timestamp": "2023-10-27T11:30:00Z", "asset_url": "/assets/duck.png", "category": "bird"}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_assets": len(assets_db), "average_score": sum(a['score'] for a in assets_db) / len(assets_db)}

@app.post("/api/reviews")
def submit_review(data: dict):
    return {"status": "success", "received": data}

@app.get("/api/assets/list", response_model=List[Asset])
def list_assets():
    return assets_db

@app.post("/api/assets/upload")
def upload_asset(asset: Asset):
    assets_db.append(asset.dict())
    return {"status": "created", "id": asset.id}