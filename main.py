# uv run fastapi dev main.py

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app=FastAPI()
templates = Jinja2Templates(directory="templates")


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
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better. Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis nulla similique animi quo quidem quia excepturi, sunt magni aut voluptatum! Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis nulla similique animi quo quidem quia excepturi, sunt magni aut voluptatum!",
        "date_posted": "April 21, 2025",
    },
]



@app.get("/", include_in_schema=False, name="home")
@app.get("/home", include_in_schema=False, name="home")
def home(request:Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts":posts, "title": "Home"}
    )
    
    
    


@app.get("/posts", include_in_schema=False, name="posts") 
def show_posts(request: Request):
    return templates.TemplateResponse(
        request,
        "posts.html",
        {"posts": posts, "title": "Posts"}
    )

'''
Why use `url_for()` and name="somthing" instead of hardcoding URLs?

Instead of writing:

<a href="/posts">

you write:

<a href="{{ url_for('posts') }}">

because if you later change the route:

@app.get("/all-posts", name="posts")

your template still works automatically.

url_for() will now generate:

<a href="/all-posts">

without changing the HTML template.
'''