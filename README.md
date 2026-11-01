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

<!-- ## Supuestos

- Los tipos de ítem son: `escala_likert`, `seleccion_multiple`, `verdadero_falso`, `desarrollo` y `emparejamiento`.
- **Emparejamiento:** el esquema base no lo define, así que se agregaron dos campos a cada ítem: `premisas` (primera columna) y `pares_correctos` (por ejemplo `{"premisa": "1", "alternativa": "b"}`). Las opciones de la segunda columna van en `alternativas`. En los demás tipos estos campos van vacíos.
- **Verdadero/falso:** las alternativas se normalizan con los valores `V` y `F`.
- `respuesta_correcta` solo se completa si el documento la indica (por ejemplo en una clave de respuestas); el modelo no resuelve los ítems.
- Si una escala se indica una sola vez para un grupo de ítems, se repite en cada ítem.
- Si el documento no tiene preguntas, la API responde 422 en lugar de un resultado vacío.
- El idioma lo detecta el modelo y se devuelve como código ISO (`it`, `es`, `en`, etc.).
- Los archivos se envían directamente a Gemini y se borran de su almacenamiento al terminar.
- Los documentos de prueba son inventados; no se usa material de tests comerciales ni datos personales. -->
