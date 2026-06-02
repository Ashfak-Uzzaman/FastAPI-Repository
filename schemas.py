# Import the datetime class.

from datetime import datetime

# Pydantic is used to validate and structure data in FastAPI. Import important classes from Pydantic.

# BaseModel: The parent class for creating data models.

# ConfigDict: Used to configure how Pydantic models behave.

# EmailStr: Special type that validates whether a string is a valid email.

# Field: Used to add validation rules such as min_length, max_length, etc.
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================================
# USER MODELS
# ==========================================================

# UserBase is the base user schema. It contains fields that are common to all user-related models.
class UserBase(BaseModel):

    username: str = Field(min_length=1, max_length=50)

    email: EmailStr = Field(max_length=120)



# Used when creating a new user.

class UserCreate(UserBase):
    pass


# UserResponse is used when sending user data back to the client.
# Example:
# After getting a user from the database,
# FastAPI can return it using this schema.
class UserResponse(UserBase):

    # Tells Pydantic:
    # "You may receive a SQLAlchemy object instead of a dictionary."
    #
    # Without this, Pydantic expects a dictionary like:
    # {
    #     "id": 1,
    #     "username": "John"
    # }
    #
    # With from_attributes=True,
    # it can also read attributes from SQLAlchemy objects.
    model_config = ConfigDict(from_attributes=True)

    # User ID from database.
    id: int

    # User image filename.
    # "|" means Union.
    #
    # str | None means:
    # Either a string OR None.
    #
    # Examples:
    # "profile.jpg"
    # None
    image_file: str | None

    # Full path to the image.
    # Example:
    # uploads/profile.jpg
    image_path: str


# ==========================================================
# POST MODELS
# ==========================================================

# Base schema for posts.
# Contains fields shared by multiple post schemas.
class PostBase(BaseModel):

    # Post title.
    title: str = Field(min_length=1, max_length=100)

    # Post content/body.
    content: str = Field(min_length=1)


# Used when creating a new post.
class PostCreate(PostBase):

    # ID of the user who created the post.

    user_id: int # TEMPORARY. Will use Auth. id will be get automatically later.
   


# Used when returning a post to the client.
class PostResponse(PostBase):

    # Allows reading values from SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)

    # Post ID from database.
    id: int

    # ID of the user who created the post.
    user_id: int

    # Every post response should contain a date and time indicating when the post was created or posted
    date_posted: datetime

    # Information about the author.
    #
    # Instead of only returning:
    # user_id = 1
    #
    # It can return a complete user object:
    #
    # {
    #     "id": 1,
    #     "username": "John",
    #     "email": "john@gmail.com"
    #     "image_path": profile.jpg
    #     " image_path": image/file/path
    # }
    #
    # SQLAlchemy when loads a post it can also load the related use. Pydentic sees that author field, validate the user object against `UserResponse`.
    #
    # UserResponse is called a nested schema.
    author: UserResponse