from fastapi import APIRouter, Depends, Query
from app.models import *
from app.routes import DocTags
from app.services.redis_service import RedisService
from app.dependencies import get_arq_pool

agents_api = APIRouter(
    prefix="/api/v1/agents",
)
@agents_api.post("/main", response_model=TaskAcceptedResponse, tags=[DocTags.Agents])
async def main_agent(data: AgentRequest, arq_pool=Depends(get_arq_pool)):
    """Запуск основного агента"""
    id = await RedisService.post_task(
        arq_pool=arq_pool,
        worker_function_name='run_agent',
        webhook_url=data.webhook_url,
        **{
            'user_message': data.user_message,
            'chat_id': data.chat_id,
            'new_file_tokens': data.new_file_tokens,
            'mcp_id': data.mcp_id,
            'mcp_prompt_name': data.mcp_prompt.name,
            'mcp_prompt_args': data.mcp_prompt.args,

        }
    )
    return TaskAcceptedResponse(
        task_id=id,
    )

@agents_api.get('/mcp', tags=[DocTags.Agents], response_model=TaskAcceptedResponse)
async def get_mcp(arq_pool=Depends(get_arq_pool), webhook_url = Query(...)):
    """
    Получить список доступных MCP серверов и их описание
    """
    id = await RedisService.post_task(
        arq_pool=arq_pool,
        worker_function_name='get_mcp',
        webhook_url=webhook_url,
    )
    return TaskAcceptedResponse(task_id = id)

@agents_api.get('/mcp/{mcp_id}', tags=[DocTags.Agents], response_model=TaskAcceptedResponse)
async def get_mcp_details(mcp_id: str, arq_pool=Depends(get_arq_pool), webhook_url = Query(...)):
    """
    Получить описание MCP сервера, его инстрмуентови, ресурсов и промптов
    
    :param mcp_id: id mcp сервера
    :type mcp_id: str
    """
    id = await RedisService.post_task(
        arq_pool=arq_pool,
        worker_function_name='mcp_details',
        webhook_url=webhook_url,
        id = mcp_id,
    )
    return TaskAcceptedResponse(task_id = id)