# LLM Surveys - Backend

API que recibe un cuestionario (PDF, Word o Excel) y devuelve sus ítems y alternativas en un JSON estandarizado, usando Gemini (free tier) para la extracción.

- **Deploy:** https://llm-surveys-back.onrender.com/
- **Frontend:** repositorio `llm-surveys-front`

## Stack

Python · FastAPI · Pydantic · Google Gemini (`google-genai`) · Pytest

## Instalación

```bash
python -m venv env
env\Scripts\activate        # Linux/Mac: source env/bin/activate
pip install -r requirements.txt
```

## Variables de entorno

Copia `.env.example` a `.env` y completa:

| Variable | Descripción |
|---|---|
| `GEMINI_API_KEY` | API key de Google AI Studio (gratuita) |

## Ejecución local

```bash
fastapi dev app/main.py
```

La API queda en `http://localhost:8000` y la documentación interactiva en `http://localhost:8000/docs`.

## Uso

`POST /api/v1/analysis/` con `multipart/form-data` y el campo `file` (`.pdf`, `.docx` o `.xlsx`, máximo 10 MB).

```bash
curl -X POST http://localhost:8000/api/v1/analysis/ -F "file=@examples/cuestionario_ejemplo_es.docx"
```

### Errores

| Código | Causa |
|---|---|
| 400 | Archivo sin nombre o vacío |
| 413 | Archivo mayor a 10 MB |
| 415 | Extensión o tipo de archivo no permitido |
| 422 | No se detectaron ítems o no se pudo interpretar el documento |
| 429 | Límite de uso de Gemini alcanzado |
| 502 / 503 / 504 | Servicio de IA no disponible, saturado o con timeout |

## Tests

```bash
pytest
```

Cubren la validación del archivo (extensión, vacío, tamaño) y el esquema de salida.

## Ejemplos

La carpeta `examples/` contiene cuestionarios inventados en PDF (italiano), Word (español) y Excel (inglés), junto con el JSON resultante.
