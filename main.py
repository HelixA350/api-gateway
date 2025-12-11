from fastapi import FastAPI
from app.routes.files_api import files_api
from app.routes.general_api import general_api
from app.routes.agents_api import agents_api
from arq import create_pool
from app.services.redis_service import redis_settings

app = FastAPI(
    title='API Шлюз для Работы с ИИ Агентами',
    version='0.1'
)
async def startup():
    app.state.arq_pool = await create_pool(redis_settings)
app.add_event_handler("startup", startup)

app.include_router(general_api)
app.include_router(files_api)
app.include_router(agents_api)



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)