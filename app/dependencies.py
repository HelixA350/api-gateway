# dependencies.py
from fastapi import Depends, Request

async def get_arq_pool(request: Request):
    return request.app.state.arq_pool