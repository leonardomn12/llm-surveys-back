import logging
import os
from pathlib import Path

from analysis.prompts import SURVEY_PROMPT
from analysis.schemas import AnalysisResponse
from core.client import analyze_file
from core.config import settings
from exceptions.exceptions import AIServiceException, NotItemException
from fastapi import HTTPException, UploadFile, status

ALLOW_EXTENSIONS = [".pdf", ".xlsx", ".docx"]

ALLOWS_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
]

logger = logging.getLogger(__name__)


class AnalysisService:
    @staticmethod
    def validate_extension(filename: str | None) -> None:
        if not filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo no tiene nombre",
            )

        extension = Path(filename).suffix.lower()

        if extension not in ALLOW_EXTENSIONS:
            logger.warning("Extensión no válida: %s", extension or "(sin extensión)")
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Archivo no permitido",
            )

    @staticmethod
    def validate_size(file: UploadFile) -> None:
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)

        if size == 0:
            logger.warning("Archivo vacío: %s", file.filename)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo está vacío",
            )

        if size > settings.max_file_size:
            logger.warning(
                "Archivo demasiado grande: %s (%d bytes)", file.filename, size
            )
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                detail=f"El archivo supera el máximo de {settings.max_file_size // (1024 * 1024)} MB",
            )

    def analyze_docs(self, file: UploadFile) -> AnalysisResponse:
        self.validate_extension(file.filename)
        self.validate_size(file)

        if file.content_type not in ALLOWS_TYPES:
            logger.warning(f"No puede subir un archivo tipo {file.content_type}")
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Archivo no permitido",
            )

        try:
            analysis = analyze_file(
                file.file, file.content_type, SURVEY_PROMPT, AnalysisResponse
            )
        except (AIServiceException, NotItemException) as e:
            raise HTTPException(status_code=e.status_code, detail=e.message) from e

        logger.info(f"Archivo cargado con éxito {file.filename}")

        return analysis
