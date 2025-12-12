from pydantic import BaseModel, Field, HttpUrl
from typing import Literal, Optional, Dict

# - Работы с файлами -
class PrecievedURLRequest(BaseModel):
    file_name: str
class PresignedURLResponse(BaseModel):
    presigned_url: str
    file_token: str
    expires_in: int
class FileUploadResponse(BaseModel):
    file_token: str
    message: str = Field(default='Файл успешно загружен')

# - Предобработка файла - 
class FilePreprocessingRequest(BaseModel):
    file_token: str
    processing_type: Literal['Doc2Vec', 'AudioProc']
    webhook_url: HttpUrl

class TaskAcceptedResponse(BaseModel):
    message: str = Field(default='Задача принята в работу')
    task_id: str

# - Анализ встреч -
class MeetingAnalysisRequest(BaseModel):
    processed_audio_token: str
    chat_link: Optional[str] = None
    with_tasks: bool = False
    webhook_url: HttpUrl

# - Чат с документами -
class Message(BaseModel):
    role: Literal['human', 'ai']
    content: str
class ChatWithDocRequest(BaseModel):
    collection_ids: list[str]
    messages: list[Message]
    webhook_url: HttpUrl

# - Глубокое извлечение информации из документов -
class DocumentExtractionRequest(BaseModel):
    collection_ids: list[str]
    analysis_schema_id: str
    webhook_url: HttpUrl

class PromptInput(BaseModel):
    name: str
    args: Dict[str, str]

# - Агент - 
class AgentRequest(BaseModel):
    mcp_id: Optional[str] = None
    mcp_prompt: PromptInput
    user_message: str
    new_file_tokens: Optional[list[str]] = None
    chat_id: Optional[str] = None

    webhook_url: HttpUrl