from fastapi import FastAPI
from fastapi.responses import HTMLResponse # To tell FastAPI to send the response with the text/html content type so the browser renders it as HTML.
# uv run fastapi dev main.py

# 'posts' is a list if dictionary
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

app=FastAPI()

@app.get("/")
@app.get("/Assalamualaikum") # Can appear in 2 routes: "/" and "/Assalamualaikum"
def home():
    return {"message":"Assalamualaikum! How are you?"}



@app.get("/hello", include_in_schema=False) # hide this route from the docs (http://127.0.0.1:8000/docs)
def hello():
    return {"message":"hello world!!!"}



@app.get("/api/posts")
def get_posts():
    return posts


# Send the response with the text/html content type so the browser renders it as HTML.
@app.get("/feed", response_class=HTMLResponse) 
def show_feed():
    return f'''
<h1>{posts[0]['title']}</h1>
<h4>{posts[0]['author']}</h4>
<p>{posts[0]['content']}</p>

<br>

<h1>{posts[1]['title']}</h1>
<h4>{posts[1]['author']}</h4>
<p>{posts[1]['content']}</p>
'''