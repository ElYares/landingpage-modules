import strawberry
from strawberry.scalars import JSON
from sqlalchemy.orm import Session

from .types import BusinessType, PageType
from ..services.business_service import get_business_by_slug, create_business
from ..services.page_service import get_page, create_page, update_page_recipe, publish_page
from ..recipes.validator import validate_recipe


def _to_business_type(b) -> BusinessType:
    return BusinessType(
        id=b.id, name=b.name, slug=b.slug, created_at=b.created_at
    )

def _to_page_type(p) -> PageType:
    return PageType(
        id=p.id,
        business_id=p.business_id,
        slug=p.slug,
        title=p.title,
        status=p.status,
        recipe=p.recipe,
        published_at=p.published_at,
        created_at=p.created_at,
        updated_at=p.updated_at,
    )

@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"

    @strawberry.field
    def business(self, info, slug: str) -> BusinessType | None:
        db: Session = info.context["db"]
        b = get_business_by_slug(db, slug)
        return _to_business_type(b) if b else None

    @strawberry.field
    def page(self, info, business_slug: str, page_slug: str) -> PageType | None:
        db: Session = info.context["db"]
        p = get_page(db, business_slug, page_slug)
        return _to_page_type(p) if p else None

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_business(self, info, name: str, slug: str) -> BusinessType:
        db: Session = info.context["db"]
        b = create_business(db, name=name, slug=slug)
        return _to_business_type(b)

    @strawberry.mutation
    def create_page(self, info, business_slug: str, slug: str, title: str = "Landing") -> PageType:
        db: Session = info.context["db"]
        p = create_page(db, business_slug=business_slug, slug=slug, title=title)
        return _to_page_type(p)

    @strawberry.mutation
    def update_page_recipe(self, info, business_slug: str, page_slug: str, recipe: JSON) -> PageType:
        db: Session = info.context["db"]
        validated = validate_recipe(recipe)  # <-- aquí
        p = update_page_recipe(db, business_slug=business_slug, page_slug=page_slug, recipe=validated)
        return _to_page_type(p)


    @strawberry.mutation
    def publish_page(self, info, business_slug: str, page_slug: str) -> PageType:
        db: Session = info.context["db"]
        p = publish_page(db, business_slug=business_slug, page_slug=page_slug)
        return _to_page_type(p)

    @strawberry.mutation
    def publish_page(self, info, business_slug: str, page_slug: str) -> PageType:
        db: Session = info.context["db"]

        p = get_page(db, business_slug, page_slug)
        if not p:
            raise ValueError("page not found")

        validate_recipe(p.recipe)  # <-- si falla, NO publica

        p = publish_page(db, business_slug=business_slug, page_slug=page_slug)
        return _to_page_type(p)


schema = strawberry.Schema(query=Query, mutation=Mutation)

