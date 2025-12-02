from fastapi import APIRouter, UploadFile, File, HTTPException
from enum import Enum
import uuid
from app.services.file_service import minio_client, MINIO_BUCKET
from minio.error import S3Error
import io

api = APIRouter(
    prefix="/api/v1",
)

# Теги для документации
class DocTags(str, Enum):
    General = "General"
    Files = "Files"
    Agents = "Agents"
    Tasks = "Tasks"

# - Общие маршруты -
@api.get("/health", tags=[DocTags.General])
async def health():
    return {
        "status": "alive"
    }
@api.get("/ready", tags=[DocTags.General])
async def ready():
    return {
        "status": "ready"
    }

# - Файловые маршруты -
@api.post('/files/upload', tags=[DocTags.Files])
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    object_name = f"file_{file_id}"

    try:
        content = await file.read()
        file_size = len(content)

        if file_size == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        file_data = io.BytesIO(content)

        # Загружаем в MinIO
        minio_client.put_object(
            bucket_name=MINIO_BUCKET,
            object_name=object_name,
            data=file_data,
            length=file_size,
            content_type=file.content_type or "application/octet-stream"
        )

        return {
            "file_id": file_id,
            "filename": file.filename,
            "size": file_size,
            "message": "File uploaded successfully"
        }

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO upload failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        
