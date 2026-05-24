# SQLAlchemy is a comprehensive, open-source SQL toolkit and Object-Relational Mapper (ORM) for the Python.
# Import different SQLAlchemy data types and tools
#
# Column   -> used to create table columns
# Integer  -> integer number type
# String   -> text/varchar type
# Float    -> decimal number type
from sqlalchemy import Column, Integer, String, Float


# Import declarative_base
#
# declarative_base() creates a base class.
#
# All database model classes will inherit from this Base class.
#
# SQLAlchemy uses this Base class to:
#   - understand which classes are database tables
#   - collect table information
#   - generate SQL tables later
from sqlalchemy.ext.declarative import declarative_base


# Create the Base class
#
# Think of Base as the "parent class"
# for all database models/tables.
Base = declarative_base()


# Create a class named Product
#
# class Product(Base)
# means:
# Product inherits from Base.
#
# Because of this inheritance,
# SQLAlchemy knows this class represents a database table.
class Product(Base):


    # Name of the database table
    #
    # SQLAlchemy will create a table named:
    # "products"
    #
    # Double underscore (__tablename__)
    # is a special SQLAlchemy variable.
    __tablename__ = "products"


    # Create a column named "id"
    #
    # Column(...) means:
    # this variable becomes a database column.
    #
    # Integer:
    # data type is integer
    #
    # primary_key=True:
    # makes this column the PRIMARY KEY
    #
    # Primary Key:
    #   - uniquely identifies each row
    #   - cannot be duplicated
    #   - usually auto increments
    #
    # index=True:
    # creates a database index on this column
    # which makes searching faster.
    id = Column(Integer, primary_key=True, index=True)


    # Create a column named "name"
    #
    # String:
    # stores text
    #
    # index=True:
    # create index for faster searching/filtering
    # on product names.
    name = Column(String, index=True)


    # Create a column named "description"
    #
    # Stores product description text.
    #
    # No index here because usually
    # descriptions are not searched frequently.
    description = Column(String)


    # Create a column named "price"
    #
    # Float:
    # used for decimal numbers
    #
    # Example:
    # 99.99
    # 15.5
    price = Column(Float)


    # Create a column named "quantity"
    #
    # Integer:
    # stores whole numbers
    #
    # Example:
    # 5
    # 100
    # 250
    #
    # Usually used for stock amount.
    quantity = Column(Integer)
    
    
    
class User(Base):
    
    __tablename__ = "users"
    
    u_id = Column(Integer, primary_key = True, index = True)
    u_name = Column(String, index=True)
    address = Column(String)
    
    
