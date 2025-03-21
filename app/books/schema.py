from typing import Optional
from pydantic import BaseModel, Field
from typing_extensions import Annotated

# Example descriptions for better documentation
BOOK_TITLE_EXAMPLE = "The Great Gatsby"
AUTHOR_NAME_EXAMPLE = "F. Scott Fitzgerald"
RATING_EXAMPLE = 4.5
AGE_EXAMPLE = 44


# -------------------------------
# Author Schema
# -------------------------------
class AuthorSchema(BaseModel):
    name: str = Field(example=AUTHOR_NAME_EXAMPLE)
    age: Annotated[Optional[int], Field(ge=18, le=120, example=AGE_EXAMPLE)]


# -------------------------------
# Book Schema
# -------------------------------
class BookSchema(BaseModel):
    title: str = Field(example=BOOK_TITLE_EXAMPLE)
    rating: Annotated[Optional[float], Field(ge=0.0, le=5.0, example=RATING_EXAMPLE)]
    author_id: int = Field(example=1)
