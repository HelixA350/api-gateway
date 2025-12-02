from app.routes import DocTags
from fastapi import UploadFile, File, HTTPException, APIRouter
import uuid
from app.services.file_service import minio_client, MINIO_BUCKET
from minio.error import S3Error
from app.models import * 
from datetime import timedelta

files_api = APIRouter(
    prefix="/api/v1/files",
)

# - Файловые маршруты -
@files_api.post('/upload', tags=[DocTags.Files], response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    file_token = str(uuid.uuid4())
    object_name = f"file_{file_token}"

    try:
        presigned_url = minio_client.presigned_put_object(
            bucket_name=MINIO_BUCKET,
            object_name=object_name,
            expires=timedelta(minutes=60),
        )
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO upload failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    return FileUploadResponse(
        presigned_url=presigned_url,
        file_token=file_token,
        expires_in=3600,
    )
       