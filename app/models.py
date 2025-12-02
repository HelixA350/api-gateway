from pydantic import BaseModel, Field
from typing import Literal

class FileUploadResponse(BaseModel):
    presigned_url: str
    file_token: str
    expires_in: int