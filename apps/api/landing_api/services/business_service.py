from sqlalchemy.orm import Session
from ..models import Business

def get_business_by_slug(db: Session, slug:str) -> Business | None:
    return db.query(Business).filter(Business.slug == slug).first()


def create_business(db: Session, name: str, slug: str) -> Business:
    existing = get_business_by_slug(db, slug)
    if existing:
        raise ValueError("Business slug alredy exists")

    
    b = Business(name=name, slug=slug)
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


