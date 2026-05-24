from fastapi import Depends, FastAPI, HTTPException
import database_models
from models import Product
from database import engine, session
from sqlalchemy.orm import Session

database_models.Base.metadata.create_all(bind=engine)
'''
# database_models.Base
# ---------------------
# "Base" is the parent class created using:
#
# Base = declarative_base()
#
# All database model classes inherit from this Base.
#
# Example:
#
# class Product(Base):
#     ...
#
# SQLAlchemy stores information about ALL tables/models
# inside Base.metadata



# .metadata
# ---------------------
# metadata contains all collected table information.
#
# It knows:
#   - table names
#   - column names
#   - data types
#   - primary keys
#   - indexes
#
# In your case it contains information about:
#
# Table: products
# Columns:
#   id
#   name
#   description
#   price
#   quantity



# .create_all(...)
# ---------------------
# create_all() tells SQLAlchemy:
#
# "Create all database tables that do not already exist."
#
# SQLAlchemy reads all table definitions from Base.metadata
# and generates SQL CREATE TABLE queries automatically.
#
# Example internally:
#
# CREATE TABLE products (
#     id INTEGER PRIMARY KEY,
#     name VARCHAR,
#     description VARCHAR,
#     price FLOAT,
#     quantity INTEGER
# );



# bind=engine
# ---------------------
# bind means:
#
# "Use this engine/database connection."
#
# engine was created earlier using:
#
# engine = create_engine(db_url)
#
# So SQLAlchemy knows WHICH database
# it should create tables inside.



# Final Meaning of this whole line:
# ---------------------
# Read all model/table definitions from Base.metadata and create those tables in the database using the provided engine connection.
database_models.Base.metadata.create_all(bind=engine)
'''


app = FastAPI()

@app.get("/")
def greet():
    return "Hello world"

def get_db():
    db = session()
    try:
        yield db # `yield` temporarily gives/provides the database session to FastAPI routes.
                 # `yield` pauses the function here temporarily. The function does NOT completely end yet. 
                 # FastAPI uses the db session first, then execution comes back below to finally.
    finally:
        db.close() # Close the database session. This releases database resources/connections.

# list of products with 4 products like phones, laptops, pens, tables
products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

def init_db():
    db = session()

    existing_count = db.query(database_models.Product).count()

    if existing_count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
        print("Database initialized with sample products.")
        
    db.close()

init_db() 

# This function will execute whenever the "/products/" endpoint is called.
@app.get("/products/")
def get_all_products(db: Session = Depends(get_db)): # parameter 'db' will contain a database "Session" object and it depends upon `get_db()` function. 
                                                     # Depends() is FastAPI's dependency injection system.
                                                     # FastAPI will: 1. call get_db(), 
                                                     # 2. get database session from yield, 
                                                     # 3. pass that session into db, 
                                                     # 4. automatically close it later.
    products = db.query(database_models.Product).all()
    
    # query() starts a database query.
    # database_models.Product is the SQLAlchemy 'Product' model/table.
    # .all() executes the query
    # and returns ALL rows from the table.
    # Internally SQLAlchemy generates SQL like: """ SELECT * FROM products; """"
    # FastAPI automatically converts Python objects into JSON response and Client/user receives product list as JSON.
    
    return products


@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    # filter() adds a WHERE condition. Example: WHERE id = 5
    # .first() = return ONLY the first matching row.
    # If no row exists, the query returns None
    # Internally SQL looks similar to: """ SELECT * FROM products WHERE id = 5 LIMIT 1 """
    if product:
        return product
    
    return {"error": "Product not found"}


# Create data -> put
@app.post("/products/")
def create_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit() # commit() tells SQLAlchemy: "Execute all pending INSERT/UPDATE/DELETE queries and permanently save them."
    return {"message": "Product created successfully", "product": product}


# Update data -> put
@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit() 
    db.refresh(db_product) # reloads the object data from the database again. Fetch the latest version of this row from the database and update this Python object.
    return {"message": "Product updated successfully", "product": db_product}


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}