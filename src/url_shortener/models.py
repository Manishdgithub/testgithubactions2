from datetime import datetime, timezone
from pydantic import BaseModel, HttpUrl
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class URLItem(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    short_code: Mapped[str] = mapped_column(
        String(8), unique=True, index=True, nullable=False
    )
    original_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class ShortenRequest(BaseModel):
    url: HttpUrl


class ShortenResponse(BaseModel):
    short_code: str
    original_url: str


class AnalyticsResponse(BaseModel):
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime
