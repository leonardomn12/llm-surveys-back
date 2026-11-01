from io import BytesIO

import pytest
from analysis.service import AnalysisService
from core.config import settings
from fastapi import HTTPException, UploadFile


def make_upload(content: bytes = b"%PDF-1.4 content") -> UploadFile:
    return UploadFile(file=BytesIO(content), filename="survey.pdf")


@pytest.mark.parametrize(
    "filename", ["survey.pdf", "SURVEY.PDF", "survey.final.docx", "survey.xlsx"]
)
def test_valid_extension_is_accepted(filename):
    AnalysisService.validate_extension(filename)


@pytest.mark.parametrize("filename", ["survey.exe", "no_extension", "survey.pdf.exe"])
def test_invalid_extension_returns_415(filename):
    with pytest.raises(HTTPException) as exc:
        AnalysisService.validate_extension(filename)

    assert exc.value.status_code == 415


def test_missing_filename_returns_400():
    with pytest.raises(HTTPException) as exc:
        AnalysisService.validate_extension(None)

    assert exc.value.status_code == 400


def test_empty_file_returns_400():
    with pytest.raises(HTTPException) as exc:
        AnalysisService.validate_size(make_upload(b""))

    assert exc.value.status_code == 400


def test_file_over_limit_returns_413(monkeypatch):
    monkeypatch.setattr(settings, "max_file_size", 10)

    with pytest.raises(HTTPException) as exc:
        AnalysisService.validate_size(make_upload(b"x" * 11))

    assert exc.value.status_code == 413
