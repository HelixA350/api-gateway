from fastapi import FastAPI
from app.routes.files_api import files_api
from app.routes.general_api import general_api 


app = FastAPI(
    title='API Шлюз для Работы с ИИ Агентами',
    version='0.1'
)
app.include_router(general_api)
app.include_router(files_api)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)