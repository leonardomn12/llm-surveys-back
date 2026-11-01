from pydantic import ValidationError
import pytest

from analysis.schemas import AnalysisResponse


def test_valid_response():
    payload = {
        "idioma": "es",
        "items": [
            {
                "numero": 1,
                "enunciado": "Explique cómo organiza su semana.",
                "tipo": "desarrollo",
                "premisas": [],
                "alternativas": [],
                "respuesta_correcta": None,
                "pares_correctos": [],
            }
        ],
    }

    result = AnalysisResponse.model_validate(payload)

    assert result.idioma == "es"
    assert len(result.items) == 1
    assert result.total_items == 1


def test_empty_list_is_rejected():
    payload = {"idioma": "es", "items": []}

    with pytest.raises(ValidationError) as exc:
        AnalysisResponse.model_validate(payload)

    assert exc.value.errors()[0]["loc"] == ("items",)
