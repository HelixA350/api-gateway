from fastapi import APIRouter
from app.models import *
from app.routes import DocTags

agents_api = APIRouter(
    prefix="/api/v1/agents",
)

# - Агент обработки встреч -
@agents_api.post("/meeting-analysis", response_model=TaskAcceptedResponse, tags=[DocTags.Agents])
async def analyze_meetings(data: MeetingAnalysisRequest):
    """Анализ встреч. Извлечение ключевых моментов и постановка задач"""
    #TODO: здесь мы будем класть файл в очередь на обработку
    return TaskAcceptedResponse(
        task_id='dfj7yd'
    )

# - Агент чата с документами -
@agents_api.post("/document-chat", response_model=TaskAcceptedResponse, tags=[DocTags.Agents])
async def analyze_meetings(data: ChatWithDocRequest):
    """Чат с документами. 
    Агент принимает уже загруженные и предобработанные документы
    """
    #TODO: здесь мы будем класть файл в очередь на обработку
    return TaskAcceptedResponse(
        task_id='dfj7yd'
    )

# - Агент чата с документами -
@agents_api.post("/document-extraction", response_model=TaskAcceptedResponse, tags=[DocTags.Agents])
async def analyze_meetings(data: DocumentExtractionRequest):
    """Глубокое извлечение информации из документов
    Агент принимает уже загруженные и предобработанные документы.
    """
    #TODO: здесь мы будем класть файл в очередь на обработку
    return TaskAcceptedResponse(
        task_id='dfj7yd'
    )