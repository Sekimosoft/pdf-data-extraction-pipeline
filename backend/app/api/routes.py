from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from app.config import Settings, get_settings
from app.models.schemas import ErrorResponse, ExtractResponse, Locale
from app.services.extraction import ExtractionService, get_sample_pdf_bytes

router = APIRouter(prefix="/api/v1")


def get_extraction_service(settings: Settings = Depends(get_settings)) -> ExtractionService:
    return ExtractionService(settings=settings)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/extract",
    response_model=ExtractResponse,
    responses={400: {"model": ErrorResponse}, 413: {"model": ErrorResponse}},
)
async def extract_pdf(
    file: UploadFile = File(...),
    locale: Locale = Form(default="en"),
    service: ExtractionService = Depends(get_extraction_service),
) -> ExtractResponse:
    try:
        return await service.extract(file, locale)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/sample-pdf")
async def download_sample_pdf() -> Response:
    try:
        content = get_sample_pdf_bytes()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Sample PDF not found") from exc
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="sample-invoice.pdf"'},
    )
