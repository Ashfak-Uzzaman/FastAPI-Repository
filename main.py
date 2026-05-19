# uv run fastapi dev main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app=FastAPI()
templates = Jinja2Templates(directory="templates")

# The line bellow mounts a separate ASGI application (StaticFiles) inside the main FastAPI app.
app.mount("/static", StaticFiles(directory="static"), name="assets") 
# "/static" is the URL path
# Here StaticFiles(directory="static") is a separate ASGI application.
# name="static" gives the mounted app a route name.


posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast. Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis nulla similique animi quo quidem quia excepturi, sunt magni aut voluptatum! Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis nulla similique animi quo quidem quia excepturi, sunt magni aut voluptatum!",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Ashfak",
        "title": "Hikmah- new sequre social media app",
        "content": "Hikmah, a new sequre social media app created by muslims to preserve islamic values by 'Kahf'. Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis nulla similique animi quo quidem quia excepturi, sunt magni aut voluptatum! Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis nulla similique animi quo quidem quia excepturi, sunt magni aut voluptatum!",
        "date_posted": "May 16, 2026",
    },
    {
        "id": 3,
        "author": "Subin",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better. Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis nulla similique animi quo quidem quia excepturi, sunt magni aut voluptatum! Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis nulla similique animi quo quidem quia excepturi, sunt magni aut voluptatum!",
        "date_posted": "April 21, 2025",
    },
]



@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
    request,
    "home.html",
    {"request": request}
)
    
    
    


@app.get("/posts", include_in_schema=False, name="posts") 
def show_posts(request: Request):
    return templates.TemplateResponse(
        request,
        "posts.html",
        {"posts": posts, "title": "Posts"}
    )

