# uv run fastapi dev main.py
from fastapi import FastAPI, HTTPException, Request, status

from fastapi.exceptions import RequestValidationError # Import validation error class. 
                                                      # This error happens automatically when request data is invalid

from fastapi.responses import JSONResponse # Import JSONResponse so we can manually return JSON responses

from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

# Starlette handles many low-level HTTP errors. Using Starlette's exception class catches more HTTP-related exceptions globally
# These may become Starlette HTTP exceptions:404 Not Found, 405 Method Not Allowed, 403 Forbidden, Route not found.
# FastAPI itself is built on Starlette.
from starlette.exceptions import HTTPException as StarletteHTTPException 



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )


@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int):  # post_id: int means FastAPI will automatically convert it to integer
                                                # If conversion fails -> RequestValidationError occurs automatically
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post": post, "title": title},
            )
            
    # If loop finishes and no post found: raise HTTPException manually
    # status_code=404 means "Not Found", detail message will be sent to client
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/api/posts")
def get_posts():
    return posts


@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")



################## --- Exception Handler --- ##################
'''
* FastAPI automatically raises errors (StarletteHTTPException, RequestValidationError etc).
* funnctions catche errors ( general_http_exception_handler, validation_exception_handler etc).
* functions execute and return something that is programmed.

'''


# GLOBAL HTTP EXCEPTION HANDLER
# Register a global exception handler
# This handles ALL Starlette/FastAPI HTTP exceptions
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    
     # Determine error message
    message = exception.detail if exception.detail else "An error occurred. Please check your request and try again."

    # Return JSON response for API requests
    # Check if request URL starts with "/api", then return in JSON format
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
        
    # else request is NOT API request: return HTML error page, UI response that shows error to general user
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


# VALIDATION ERROR HANDLER

# Register handler for validation errors
#
# This exception occurs automatically when:
#
# - Wrong datatype
# - Missing required fields
# - Invalid query/path/body parameters
#
# Example:
# /api/posts/abc
#
# Here:
# post_id should be int
# but "abc" is string

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

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

