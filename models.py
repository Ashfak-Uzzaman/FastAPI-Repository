# This import allows us to use type hints of classes
# before the classes are actually created.
# Example: User class can use Post type before Post exists.
from __future__ import annotations


# Import datetime-related tools from Python's datetime module.
# UTC = Universal Time Coordinate (Zone)
# datetime = used for date and time objects
from datetime import UTC, datetime


# Import SQLAlchemy column data types and helpers.
# These are used to define database table columns.
from sqlalchemy import (
    DateTime,   # Stores date and time
    ForeignKey, # Creates relationship between tables
    Integer,    # Integer number type
    String,     # String/VARCHAR type
    Text        # Large text type
)

# Import ORM-related tools from SQLAlchemy.
from sqlalchemy.orm import (
    Mapped,         # Used for type-safe ORM mapping
    mapped_column,  # Used to create table columns. mapped_column() is the modern replacement for Column() in ORM models.
    relationship    # Used to create relationships between tables
)


# Import Base class from database.py
# Every model/table class will inherit from Base.
from database import Base



# -----------------------------
# USER TABLE MODEL
# -----------------------------
class User(Base):

    # Name of the table inside the database
    __tablename__ = "users"

    # -- Id column -- #
    
    # Mapped[int] → Gives Python Type Information. This tells Python and tools like VS Code: id will contain an int
    # So thr editor can: give better autocomplete, detect type errors, improve readability
    id: Mapped[int] = mapped_column( # mapped_column() is the modern replacement for Column() in ORM models.
        Integer,
        primary_key=True, # Primary key column # primary_key=True means unique ID for each row
        index=True # index=True makes searching faster
    )


    # -- Username column -- #
    
    username: Mapped[str] = mapped_column(
        String(50), # String length maximum = 50 characters
        unique=True, # unique=True means no duplicate usernames allowed
        nullable=False # nullable=False means this field is required
    )


    #  -- Email column -- #
     
    email: Mapped[str] = mapped_column(
        String(120),
        unique=True, # unique=True means every email must be different
        nullable=False # nullable=False means cannot be empty
    )


    # -- image_file column -- #
    
    # str | None means: Can store string Or can store None (NULL in database)
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True, # nullable=True means optional field
        default=None, # default=None means default value is NULL
    )

    # -- One to Many relationship -- #
    # -- Relationship with Post table. One user can have many posts. So posts will contain a list of Post objects.
    # `back_populates="author"` connects this relationship with Post.author relationship
    # relationship() creates the connection in Python objects, not in database. It runs inside RAM.
    posts: Mapped[list[Post]] = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan",
    )
    
    # -- Relationship (User object points to Post objects) -- #
    '''
    |====|------> |Post-1|
    |User|------> |Post-2| 
    |====|------> |Post-3|
    '''
    # cascade="all, delete-orphan" destroys all Post objects related to the specific User Object


    # @property allows calling this method like an attribute
    # Example: user.image_path instead of: user.image_path()
    @property
    def image_path(self) -> str:

        # If user uploaded image exists
        if self.image_file:

            # Return uploaded image path
            return f"/media/profile_pics/{self.image_file}"

        # Otherwise return default profile image path
        return "/static/profile_pics/default.jpg"




# -----------------------------
# POST TABLE MODEL
# -----------------------------
class Post(Base):

    # Database table name
    __tablename__ = "posts"


    # -- Primary key for posts table -- #
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


    # -- Post title column -- #
    title: Mapped[str] = mapped_column(
        String(100), # Maximum 100 characters
        nullable=False # nullable=False means required
    )


    # Post content/body
    # Text type is used because content can be large
    # nullable=False means required
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    # -- Foreign key column -- This connects posts table with users table. 
    # ForeignKey() creates the connection in the database.
    # `ForeignKey("users.id")` means: user_id references users table's id column
    # nullable=False means every post must belong to a user. index=True improves searching/filtering speed.
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )


    # Date and time when post was created
    # default=lambda: datetime.now(UTC) automatically sets current UTC time when a new post is created
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), # timezone=True stores timezone information too
        default=lambda: datetime.now(UTC), # A lambda function that automatically sets current UTC time when a new post is created
    )


    # -- Many to One relationship -- #
    #  -- Relationship back to User table. Each post has one author/user
    # back_populates="posts" connects with User.posts relationship
    author: Mapped[User] = relationship("User",back_populates="posts")
    
    '''
    |====| <-------|Post-1|
    |User| <-------|Post-2| 
    |====| <-------|Post-3|
    '''