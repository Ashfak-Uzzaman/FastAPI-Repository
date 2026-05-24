# SQLAlchemy is a comprehensive, open-source SQL toolkit and Object-Relational Mapper (ORM) for the Python.
from sqlalchemy import create_engine # Engine means: the main connection manager between Python and the database

from sqlalchemy.orm import sessionmaker # `sessionmaker` is used to create "Session" factory (class)  for Session objects. 
                                        # Session is used to talk with the database (insert, update, delete, read)


# Database URL / connection string
# This tells SQLAlchemy:
#   - which database we are using
#   - username
#   - password
#   - host
#   - port
#   - database name
#
# Format:
# postgresql://username:password@host:port/database_name
#
# Here:
#   postgresql -> database type
#   postgres   -> username
#   0000       -> password
#   localhost  -> database server is running on this same computer
#   5432       -> PostgreSQL default port
#   ashfakdb    -> database name

database_name = "ashfakdb"
password = "1234"
db_url = f"postgresql://postgres:{password}@localhost:5432/{database_name}"


#------------------------------------------------------------#
# Create the Engine (connection manager) object
#
# Engine is responsible for:
#   - connecting Python with PostgreSQL
#   - managing database connections
#   - sending SQL queries
#
# This does NOT immediately connect permanently to the DB. It prepares everything needed for connection.
engine = create_engine(db_url)


# -------------------------------------------------------------#
# Create a "Session" factory (class)
# Every time we connect to something, it is a session.
# If we connect to a server that's one session.
# If we connect to a database that's one session.

# `sessionmaker()` creates "Session" factory (class)  for Session objects. 
# "Session" = connection/conversation with database.
# Later we can create actual sessions (`Session object`) like: db = session()
session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Parameters:
#
# autocommit=False
# ----------------
# Changes are NOT automatically saved to the database.
# We must manually call:
#
#   db.commit()
#
# This is safer because we control when data is saved.
#
#
# autoflush=False
# ----------------
# SQLAlchemy will NOT automatically send pending changes to the database before every query.
# We manually control when data is flushed/sent.
#   db.add(new_user) # Nothing sent yet
#   db.flush()   # NOW send to DB manually
#
# or
#
#   db.commit()  # commit also performs flush first
#
# bind=engine
# ----------------
# Attach this Session factory to our database engine.
# Meaning:
# Sessions created from `session` will use this engine
# to communicate with PostgreSQL.

