import logging
from typing import BinaryIO, TypeVar

from core.config import settings
from exceptions.exceptions import AIServiceException, NotItemException
from google import genai
from google.genai import errors as genai_errors
from google.genai._gaos.lib.compat_errors import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

client = genai.Client(api_key=settings.gemini_api_key)

T = TypeVar("T", bound=BaseModel)


def analyze_file(file: BinaryIO, mime_type: str, prompt: str, schema: type[T]) -> T:
    file_uploaded = None
    try:
        file_uploaded = client.files.upload(file=file, config={"mime_type": mime_type})

        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=[
                {"type": "text", "text": prompt},
                {
                    "type": "document",
                    "uri": file_uploaded.uri,
                    "mime_type": file_uploaded.mime_type,
                },
            ],
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": schema.model_json_schema(),
            },
        )
        logger.info("Respuesta cruda del modelo: %s", interaction.output_text)
        return schema.model_validate_json(interaction.output_text)
    except ValidationError as e:
        logger.error("La respuesta del modelo no cumple el schema: %s", e)
        if any(err["loc"] == ("items",) for err in e.errors()):
            raise NotItemException(
                "No se encontraron ítems en el documento", 422
            ) from e
        raise AIServiceException("No se pudo interpretar el cuestionario", 422) from e
    except InternalServerError as e:
        logger.warning("Error del servicio Gemini: %s", e)
        raise AIServiceException(
            "El modelo está saturado, intenta de nuevo en unos minutos", 503
        ) from e
    except APITimeoutError as e:
        logger.warning("Timeout con Gemini: %s", e)
        raise AIServiceException(
            "El servicio de IA tardó demasiado en responder", 504
        ) from e
    except APIConnectionError as e:
        logger.warning("Error de conexión con Gemini: %s", e)
        raise AIServiceException(
            "No se pudo conectar con el servicio de IA", 502
        ) from e
    except (AuthenticationError, PermissionDeniedError) as e:
        logger.critical("Credenciales de Gemini inválidas o sin permisos: %s", e)
        raise AIServiceException("El servicio de IA no está disponible", 503) from e

    except RateLimitError as e:
        logger.warning("Cuota o límite de uso de Gemini alcanzado: %s", e)
        raise AIServiceException(
            "Se alcanzó el límite de uso del servicio de IA, intenta más tarde", 429
        ) from e
    except BadRequestError as e:
        logger.error("Gemini rechazó la petición: %s", e)
        raise AIServiceException(
            "El servicio de IA no pudo procesar el documento", 422
        ) from e
    except NotFoundError as e:
        logger.error("Modelo o archivo no encontrado en Gemini: %s", e)
        raise AIServiceException("El servicio de IA no está disponible", 503) from e
    except APIStatusError as e:
        logger.error("Error inesperado de Gemini (%s): %s", e.status_code, e)
        raise AIServiceException("Error en el servicio de IA", 502) from e
    except genai_errors.APIError as e:
        logger.error("Error de Gemini al subir el archivo (%s): %s", e.code, e)
        status_code = 429 if e.code == 429 else 503 if e.code >= 500 else 502
        raise AIServiceException(
            "No se pudo enviar el documento al servicio de IA", status_code
        ) from e
    finally:
        if file_uploaded:
            try:
                client.files.delete(name=file_uploaded.name)
            except genai_errors.APIError as e:
                logger.warning(
                    "No se pudo borrar el archivo %s de Gemini: %s",
                    file_uploaded.name,
                    e,
                )
