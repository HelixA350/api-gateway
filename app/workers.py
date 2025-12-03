from enum import Enum
from pydantic import BaseModel, Field

class Workers(Enum):
    load_doc_for_rag = 'load_doc_for_rag'
    process_audio = 'process_audio'

