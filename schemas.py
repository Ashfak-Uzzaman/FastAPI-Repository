# Import BaseModel for creating data models
# ConfigDict for model configuration
# Field for adding validation rules
from pydantic import BaseModel, ConfigDict, Field


# Base schema for a Post
class PostBase(BaseModel):

    title: str = Field(min_length=1, max_length=100)

    content: str = Field(min_length=1)

    author: str = Field(min_length=1, max_length=50)



class PostCreate(PostBase):
    pass  # No new fields — inherits everything



class PostResponse(PostBase):

    # Allows Pydantic to convert ORM objects/dicts into Pydantic models
    # Without from_attributes=True -> Pydantic expects dictionary-like data.
    # With from_attributes=True -> Pydantic can read values from object attributes too.
    # So it reads: user.name, user.age and converts them into Pydantic model.
    model_config = ConfigDict(from_attributes=True)

    # Extra fields returned in response
    id: int # For pydentic validation, we can use/named `id` though it is a built-in funnction, but here, it cannot make problem.
    date_posted: str