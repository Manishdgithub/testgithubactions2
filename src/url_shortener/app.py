from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from url_shortener.database import engine, get_db
from url_shortener.models import (
    AnalyticsResponse,
    Base,
    ShortenRequest,
    ShortenResponse,
    URLItem,
)
from url_shortener.service import create_url_mapping, get_and_increment_url


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="URL Shortener API", lifespan=lifespan)


@app.post(
    "/api/shorten",
    response_model=ShortenResponse,
    status_code=status.HTTP_201_CREATED,
)
def shorten_url(payload: ShortenRequest, db: Session = Depends(get_db)):
    record = create_url_mapping(db, str(payload.url))
    return ShortenResponse(
        short_code=record.short_code, original_url=record.original_url
    )


@app.get("/api/analytics/{short_code}", response_model=AnalyticsResponse)
def get_analytics(short_code: str, db: Session = Depends(get_db)):
    record = db.query(URLItem).filter(URLItem.short_code == short_code).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
        )
    return AnalyticsResponse(
        short_code=record.short_code,
        original_url=record.original_url,
        clicks=record.clicks,
        created_at=record.created_at,
    )


@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    record = get_and_increment_url(db, short_code)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
        )
    return RedirectResponse(
        url=record.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
