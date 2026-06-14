from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload # For Eager loading (optimized)
from starlette.exceptions import HTTPException as StarletteHTTPException

import models
from database import Base, engine, get_db
from routers import post, users


@asynccontextmanager  # Marks this function as an asynchronous context manager. FastAPI can use it to manage startup and shutdown events.
async def lifespan(
    _app: FastAPI,
):  # _app receives the FastAPI application instance. The underscore means “I am not using this parameter directly.”
    """
    When the app starts, open the database, create any missing tables, then start serving requests.
    When the app stops, close the database engine and clean up resources.
    """
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )  # Creates all database tables defined in your SQLAlchemy models if they do not already exist.
    yield  # This is the divider between startup and shutdown. FastAPI runs the app while execution is paused here.

    # Shutdown
    await engine.dispose()  # Closes the database engine and releases any remaining connections/resources during shutdown.


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(post.router, prefix="api/posts", tags=["posts"])


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]): # Note Python itself does nothing with it unless some library reads the annotation and executes the callable.
                                                                                # Python does NOT: read Annotated, call Depends, call get_db
                                                                                # Instead: FastAPI inspects the function signature,  sees Annotated[..., Depends(get_db)], 
                                                                                # then FastAPI decides to execute get_db

    result = await db.execute(
        select(
            models.Post
        ).options(  # .options(...) When fetching posts, also do something special with their related data
            selectinload(models.Post.author) # selectinload() tells SQLAlchemy: "Load the related authors in advance using a separate optimized query, so extra queries are not needed later."
        ),
    )
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )


@app.get("/post/{post_id}",include_in_schema=False)
async def post_page(request:Request, post_id:int, db:Annotated[AsyncSession, Depends(get_db)],):
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.id == post_id),
    )
    
    post = result.scalar().first()
    
    if post:
        title=post.title[:50]
        return templates.TemplateResponse(
            request,
            "post.html",
            {"post":post,"title":title},
        )
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")

    

@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
async def user_posts_page(
    request: Request,
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.user_id == user_id),
    )
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )



@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(
    request: Request,
    exception: StarletteHTTPException,
):
    if request.url.path.startswith("/api"):
        return await http_exception_handler(request, exception)

    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError,
):
    if request.url.path.startswith("/api"):
        return await request_validation_exception_handler(request, exception)

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )