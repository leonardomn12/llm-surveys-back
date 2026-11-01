from typing import Annotated

from analysis.schemas import AnalysisResponse
from analysis.service import AnalysisService
from fastapi import APIRouter, File, UploadFile, status

router = APIRouter(prefix="/analysis", tags=["Analisis"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AnalysisResponse)
def generate_analysis(file: Annotated[UploadFile, File()]):
    return AnalysisService().analyze_docs(file)
