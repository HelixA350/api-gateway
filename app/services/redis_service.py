from arq.connections import RedisSettings
import os
from pydantic import HttpUrl

redis_settings = RedisSettings(
    host=os.getenv("REDIS_HOST"),
    port = os.getenv("REDIS_PORT"),
)

class RedisService:
    @staticmethod        
    async def post_task(arq_pool, worker_function_name : str, webhook_url : HttpUrl, **kwargs) -> str:
        """Отправляет задачу в очередь и сохраняет вебхук для отправки результата в редис"""
        try:
            job = await arq_pool.enqueue_job(worker_function_name, **kwargs) # Создаем задачу
            # Сохраняем вебхук для отправки результата
            await arq_pool.setex(
                f"webhook:{job.job_id}",
                3600,
                str(webhook_url)
            )
            return job.job_id
        except Exception as e:
            raise Exception(f"Failed to post task: {e}")
