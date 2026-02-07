from typing import Any, Literal
from pydantic import BaseModel, Field, ConfigDict

SectionType = Literal["Hero", "Features", "Testimonials", "Pricing", "FAQ", "CTA", "Footer"]

class Theme(BaseModel):
    model_config = ConfigDict(extra="allow")
    primary: str | None = None
    font: str | None = None

class Section(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: SectionType
    props: dict[str, Any] = Field(default_factory=dict)

class Recipe(BaseModel):
    model_config = ConfigDict(extra="allow")
    theme: Theme = Field(default_factory=Theme)
    sections: list[Section] = Field(default_factory=list)

