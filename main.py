from fastapi import FastAPI
from app.api import api

app = FastAPI(
    title='API Шлюз для Работы с ИИ Агентами',
    version='0.1'
)

app.include_router(api)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)