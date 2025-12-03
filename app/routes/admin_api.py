from fastapi import APIRouter
from app.routes import DocTags

admin_api = APIRouter(
    prefix="/api/v1/admin"
)

@admin_api.get("/schemas", tags=[DocTags.Admin])
async def get_schemas():
    """Возвращает id схем и метаданные"""
    #TODO: будем доставать созданные схемы из postgres
    pass

@admin_api.get("/schemas/{schema_id}", tags=[DocTags.Admin])
async def get_schema(schema_id: str):
    """Возвращает всю схему по id"""
    #TODO: будем доставать конкретную схему по id
    pass
