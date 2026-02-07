from datetime import datetime
import strawberry

@strawberry.type
class BusinessType:
    id: int
    name: str
    slug: str
    created_at: datetime

@strawberry.type
class PageType:
    id: int
    business_id: int
    slug: str
    title: str
    status: str
    recipe: strawberry.scalars.JSON
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime

