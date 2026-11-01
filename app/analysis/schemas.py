from typing import Literal

from pydantic import BaseModel, Field, computed_field, field_validator

TipoItem = Literal[
    "escala_likert",
    "seleccion_multiple",
    "verdadero_falso",
    "desarrollo",
    "emparejamiento",
]


class Alternativa(BaseModel):
    valor: int | str = Field(
        description="Valor numérico (escalas) o letra/etiqueta (a, b, c, V, F)"
    )
    texto: str = Field(description="Texto literal de la opción, tal como aparece")


class ParCorrecto(BaseModel):
    premisa: str = Field(description="Valor de la premisa (columna A), ej: '1'")
    alternativa: str = Field(
        description="Valor de la alternativa correcta (columna B), ej: 'b'"
    )


class SurveyItems(BaseModel):
    numero: int
    enunciado: str = Field(description="Texto literal de la pregunta, sin reformular")
    tipo: TipoItem
    premisas: list[Alternativa] = Field(
        description="Solo emparejamiento: elementos de la primera columna. Lista vacía en los demás tipos",
    )
    alternativas: list[Alternativa] = Field(
        description="Opciones de respuesta. En emparejamiento, las de la segunda columna. Vacío en desarrollo"
    )
    respuesta_correcta: int | str | None = Field(
        description="Valor (no texto) de la alternativa correcta, solo si el documento lo indica; si no, null",
    )
    pares_correctos: list[ParCorrecto] = Field(
        description="Solo emparejamiento: pares correctos según la clave de respuestas. "
        "Lista vacía si no es emparejamiento o el documento no trae la clave",
    )

    model_config = {"from_attributes": True}


class AnalysisResponse(BaseModel):
    titulo: str | None = Field(
        default=None, description="Título del documento; null si no tiene"
    )
    idioma: str = Field(
        description="Código ISO del idioma del documento, ej: it, es, en"
    )
    items: list[SurveyItems] = Field(
        description="Preguntas del cuestionario. Lista vacía si el documento no tiene preguntas"
    )

    @field_validator("items")
    @classmethod
    def items_validos(cls, v: list[SurveyItems]) -> list[SurveyItems]:
        v = [item for item in v if item.enunciado.strip()]  # descarta ítems vacíos
        if not v:
            raise ValueError("El cuestionario debe tener al menos un ítem")
        return v

    @computed_field
    @property
    def total_items(self) -> int:
        return len(self.items)

    model_config = {"from_attributes": True}
