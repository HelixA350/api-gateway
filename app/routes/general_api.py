from app.routes import DocTags
from fastapi import APIRouter

general_api = APIRouter(
    prefix='/api/v1',
    tags=[DocTags.General]
)

# - Общие маршруты -
@general_api.get("/health", tags=[DocTags.General])
async def health():
    return {
        "status": "alive"
    }
@general_api.get("/ready", tags=[DocTags.General])
async def ready():
    return {
        "status": "ready"
    }