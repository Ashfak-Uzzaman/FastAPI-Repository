# uv run fastapi dev main.py

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

# Jinja2Templates: 
# Jinja2 is a Python templating engine used to generate dynamic HTML pages using variables, loops, conditions, and reusable layouts. 
# It lets you create dynamic HTML pages by mixing: HTML, Python-like template syntax, data from your backend.
# Jinja2Templates is a FastAPI/Starlette helper that renders dynamic HTML pages using the Jinja/Jinja2 templating engine.


app=FastAPI()
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
        "author": "Ashfak",
        "title": "Hikmah- new sequre social media app",
        "content": "Hikmah, a new sequre social media app created by muslims to preserve islamic values by 'Kahf'.",
        "date_posted": "May 16, 2026",
    },
    {
        "id": 3,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]



@app.get("/home")
@app.get("/posts", include_in_schema=False) # Can appear in 2 routes: "/" and "/Assalamualaikum"
def home(request:Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts":posts, "title": "Home"}
    )



