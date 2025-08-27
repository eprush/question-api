"""
A module that creates routers with all endpoints
"""

from fastapi import APIRouter
from src.endpoints import questions, answers

routers = APIRouter()

routers.include_router(questions.router)
routers.include_router(answers.router)