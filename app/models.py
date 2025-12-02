from pydantic import BaseModel, Field
from typing import Literal

class FileUploadResponse(BaseModel):
    file_id: str
    file_name: str
    bytes_size: int
    message: str = Field(default="File uploaded successfully")