from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
import logging
from db_manager import DatabaseManager
from fastapi import HTTPException
from datetime import datetime
import uvicorn
import models
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
POSTGRES_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@postgres:5432/"
LOGS_DB_NAME = "logs"
AUTHORS_DB_NAME = "authors"
PORT = int(os.getenv("API_PORT", 1860))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("API")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting database manager...")
        app.state.db_manager = DatabaseManager(POSTGRES_URL + AUTHORS_DB_NAME, POSTGRES_URL + LOGS_DB_NAME)
        await app.state.db_manager.init_db()
        logger.info("Database manager started successfully.")
        yield
        logger.info("Shutting down database manager...")
        await app.state.db_manager.close_db()
        logger.info("Database manager shut down successfully.")
    except Exception as e:
        logger.error(f"Error during database manager initialization: {e}")
        raise e

app = FastAPI(lifespan=lifespan)

@app.get("/api/general", response_model=models.GeneralResponse)
async def get_general(login: str) -> models.GeneralResponse:
    try:
        response = await app.state.db_manager.get_general(login)
        return models.GeneralResponse(data=[models.GeneralResponseItem(**item) for item in response])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/comments", response_model=models.CommentsResponse)
async def get_general(login: str) -> models.CommentsResponse:
    try:
        response = await app.state.db_manager.get_comments(login)
        return models.CommentsResponse(data=[models.CommentsResponseItem(**item) for item in response])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "manager_initialized": getattr(app.state, "db_manager", None) is not None,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)