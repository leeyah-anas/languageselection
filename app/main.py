from fastapi import FastAPI
from datetime import datetime

from .core.config import settings
from app.db.base import Base, engine
from app.api import api_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="API for managing user preferences for learning Hausa language",
)


app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "language preference"}
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
