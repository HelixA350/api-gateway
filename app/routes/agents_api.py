from fastapi import APIRouter, Depends
from app.models import *
from app.routes import DocTags
from app.services.redis_service import RedisService
from app.dependencies import get_arq_pool

agents_api = APIRouter(
    prefix="/api/v1/agents",
)

# - Агент обработки встреч -
@agents_api.post("/meeting-analysis", response_model=TaskAcceptedResponse, tags=[DocTags.Agents])
async def analyze_meetings(data: MeetingAnalysisRequest, arq_pool=Depends(get_arq_pool)):
    """Анализ встреч. Извлечение ключевых моментов и постановка задач"""
    #TODO: здесь мы будем класть файл в очередь на обработку
    id = await RedisService.post_task(
        arq_pool=arq_pool,
        worker_function_name='analyze_meeting',
        webhook_url=data.webhook_url,
        **{
            'processed_audio_token': data.processed_audio_token,
            'chat_link': data.chat_link,
            'with_tasks': data.with_tasks,
        }
    )
    return TaskAcceptedResponse(
        task_id=id,
    )

# - Агент чата с документами -
@agents_api.post("/document-chat", response_model=TaskAcceptedResponse, tags=[DocTags.Agents])
async def analyze_meetings(data: ChatWithDocRequest, arq_pool=Depends(get_arq_pool)):
    """Чат с документами. 
    Агент принимает уже загруженные и предобработанные документы
    """
    #TODO: здесь мы будем класть файл в очередь на обработку
    id = await RedisService.post_task(
        arq_pool=arq_pool,
        worker_function_name='chat_with_doc',
        webhook_url=data.webhook_url,
        **{
            'collection_ids': data.collection_ids,
            'messages': data.messages,
        }
    )
    return TaskAcceptedResponse(
        task_id=id,
    )
# - Агент чата с документами -
@agents_api.post("/document-extraction", response_model=TaskAcceptedResponse, tags=[DocTags.Agents])
async def analyze_meetings(data: DocumentExtractionRequest, arq_pool=Depends(get_arq_pool)):
    """Глубокое извлечение информации из документов
    Агент принимает уже загруженные и предобработанные документы.
    """
    #TODO: здесь мы будем класть файл в очередь на обработку
    id = await RedisService.post_task(
        arq_pool=arq_pool,
        worker_function_name='deep_extract_data',
        webhook_url=data.webhook_url,
        **{
            'collection_ids': data.collection_ids,
            'analysis_schema_id': data.analysis_schema_id,
        }
    )
    return TaskAcceptedResponse(
        task_id=id,
    )