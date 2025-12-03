from app.routes import DocTags
from fastapi import UploadFile, File, HTTPException, APIRouter, Depends
import uuid
from app.services.file_service import minio_client, MINIO_BUCKET
from minio.error import S3Error
from app.models import * 
from datetime import timedelta
import io
from app.dependencies import get_arq_pool

files_api = APIRouter(
    prefix="/api/v1/files",
)

# - Получение подписанной ссылки для загрузки большого файла -
@files_api.post('/presigned_url', tags=[DocTags.Files], response_model=PresignedURLResponse)
async def get_presigned_url(data: PrecievedURLRequest):
    """Загрузка больших файлов (>5мб) осуществляется через presigned_url. 
    напрямую в Объектное Хранилище
    """
    file_token = str(uuid.uuid4())
    object_name = f"file_{file_token}"

    try:
        presigned_url = await minio_client.presigned_put_object(
            bucket_name=MINIO_BUCKET,
            object_name=object_name,
            expires=timedelta(minutes=10),
        )
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO upload failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    return PresignedURLResponse(
        presigned_url=presigned_url,
        file_token=file_token,
        expires_in=600,
    )

# - Загрузка маленьких файлов напрямую через шлюз -
@files_api.post('/upload', tags=[DocTags.Files], response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Загрузка маленьких файлов (<5мб)"""
    # Проверка размера файла
    size = file.size
    if size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the limit of 5MB")
    file_token = str(uuid.uuid4())
    object_name = f"file_{file_token}"

    try:
        await minio_client.put_object(
            bucket_name=MINIO_BUCKET,
            object_name=object_name,
            data=io.BytesIO(file.file.read()),
            length=size,
        )
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO upload failed: {str(e)}")
    return FileUploadResponse(
        file_token=file_token,
    )
    
# - Запрос на предобработку файла - 
@files_api.post(
        '/process',
        tags=[DocTags.Files],
        response_model=TaskAcceptedResponse,
    )
async def process_file(data: FilePreprocessingRequest, arc_pull=Depends(get_arq_pool)):
    """Предобработка файла для дальнейшего использования"""
    id = str(uuid.uuid4())
    #TODO: здесь мы будем класть файл в очередь на обработку
    await arc_pull.enqueue_job('process_file', id)
    return TaskAcceptedResponse(
        task_id = id
    )
