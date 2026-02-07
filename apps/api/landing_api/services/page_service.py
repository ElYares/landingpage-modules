from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Business, Page
from .business_service import get_business_by_slug

def get_page(db: Session, business_slug: str, page_slug: str) -> Page | None:
    b = get_business_by_slug(db, business_slug)
    if not b:
        return None
    return (
        db.query(Page)
        .filter(Page.business_id == b.id, Page.slug == page_slug)
        .first()
    )

def create_page(db: Session, business_slug: str, slug: str, title: str) -> Page:
    b = get_business_by_slug(db, business_slug)
    if not b:
        raise ValueError("business not found")

    existing = (
        db.query(Page)
        .filter(Page.business_id == b.id, Page.slug == slug)
        .first()
    )
    if existing:
        raise ValueError("page slug already exists for business")

    p = Page(business_id=b.id, slug=slug, title=title, status="DRAFT", recipe={})
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def update_page_recipe(db: Session, business_slug: str, page_slug: str, recipe: dict) -> Page:
    p = get_page(db, business_slug, page_slug)
    if not p:
        raise ValueError("page not found")

    p.recipe = recipe
    db.commit()
    db.refresh(p)
    return p

def publish_page(db: Session, business_slug: str, page_slug: str) -> Page:
    p = get_page(db, business_slug, page_slug)
    if not p:
        raise ValueError("page not found")

    p.status = "PUBLISHED"
    p.published_at = datetime.utcnow()
    db.commit()
    db.refresh(p)
    return p

