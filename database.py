# Import create_engine function from SQLAlchemy
# create_engine() is used to create a connection between Python and the database
from sqlalchemy import create_engine 


# Import DeclarativeBase and sessionmaker from SQLAlchemy ORM
# DeclarativeBase -> used to create a base class for database models/tables
# sessionmaker -> used to create database session objects
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Database URL / connection string
# "sqlite:///./blog.db" means:
# sqlite      -> use SQLite database
# ///         -> relative file path
# ./blog.db   -> create/find blog.db file in current project folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"


# Create the database engine
# Engine is the main object that manages communication with the database
engine = create_engine(

    # Pass the database URL to the engine
    SQLALCHEMY_DATABASE_URL,

    # Extra connection settings for SQLite
    connect_args={"check_same_thread": False},
    
    # SQLite normally allows only the same thread that created
    # the connection to use it.
    # FastAPI handles requests using multiple threads,
    # so we disable this restriction by setting False.
)


# This is a factory to create a Session. A Session is essentially a transaction with the database.
# sessionmaker() does NOT create a session immediately.
# Instead, it creates a "session generator/factory".
# Later, SessionLocal() will create actual session objects.
SessionLocal = sessionmaker(

    # autocommit=False means:
    # changes are NOT automatically saved to the database
    # You must manually call:
    # db.commit()
    autocommit=False,

    # autoflush=False means:
    # SQLAlchemy will NOT automatically send changes
    # to the database before queries
    autoflush=False,

    # Bind this session factory to the engine
    # so all sessions know which database to use
    bind=engine
)


# Create a Base class for all database models
# Every table/model class will inherit from this Base class
# Example:
# class User(Base):
#     ...
class Base(DeclarativeBase):

    # pass means:
    # no extra code inside this class for now
    pass


# Dependency function for FastAPI
# Used to get a database session for each request
def get_db():

    # Create a new database session using SessionLocal()
    # "with" automatically closes the session after use
    with SessionLocal() as db:

        # yield sends the db session to FastAPI route functions
        # Example:
        # def route(db: Session = Depends(get_db))
        yield db

        # After request finishes,
        # the session is automatically closed
        