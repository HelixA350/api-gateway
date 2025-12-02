from fastapi import APIRouter
from enum import Enum

# Теги для документации
class DocTags(str, Enum):
    General = "General"
    Files = "Files"
    Agents = "Agents"
    Tasks = "Tasks"

