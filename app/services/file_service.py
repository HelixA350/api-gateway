# minio_client.py
from minio import Minio
import os

minio_client = Minio(
    os.getenv('MINIO_ENDPOINT'),
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
    secure=False,
)

MINIO_BUCKET = os.getenv('MINIO_BUCKET')