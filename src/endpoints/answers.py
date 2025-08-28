"""
A module that implements endpoints of the type /answers
"""


from fastapi import APIRouter, status, HTTPException


#from src.core.dependecies import (
    #AnimalServiceDependence,
    #ImageServiceDependence,
    #EmailServiceDependence,
#)
# src.schemas.animal import (
    #AnimalSchema,
    #AnimalTypeSchema,
#)
#from src.schemas.problem import ProblemDetail


router = APIRouter(prefix="/answers", tags=["Работа с ответами."])