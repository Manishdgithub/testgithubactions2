import secrets
import string

from sqlalchemy.orm import Session

from url_shortener.models import URLItem

CHARACTERS = string.ascii_letters + string.digits


def generate_short_code(length: int = 6) -> str:
    return "".join(secrets.choice(CHARACTERS) for _ in range(length))


def create_url_mapping(db: Session, original_url: str) -> URLItem:
    code = generate_short_code()
    while db.query(URLItem).filter(URLItem.short_code == code).first() is not None:
        code = generate_short_code()

    record = URLItem(short_code=code, original_url=original_url)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_and_increment_url(db: Session, short_code: str) -> URLItem | None:
    record = db.query(URLItem).filter(URLItem.short_code == short_code).first()
    if record:
        record.clicks += 1
        db.commit()
        db.refresh(record)
    return record
