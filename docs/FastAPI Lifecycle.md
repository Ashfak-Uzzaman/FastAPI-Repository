# 1. Run the Command to Start App

```bash
fastapi dev main.py
```

Example app:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello"}
```

---

# 2. What Happens First?

The command:

```bash
fastapi dev main.py
```

starts the **FastAPI CLI**.

The CLI:

1. Finds `main.py`
2. Imports the file
3. Searches for a FastAPI object (`app`)
4. Starts an ASGI server (usually Uvicorn)

So internally it behaves similar to:

```bash
uvicorn main:app --reload
```

---

# 3. Python Imports `main.py`

Python now executes the whole file from top to bottom.

So this runs:

```python
app = FastAPI()
```

This creates a FastAPI application object.

Think of it like:

```python
app = FastAPI()
```

means:

> "Create a web application that can receive HTTP requests."

---

# 4. What Does `@app.get("/")` Actually Do?

This is VERY important.

Many beginners think this function runs immediately.

It does NOT.

---

When Python sees:

```python
@app.get("/")
def home():
    return {"message": "Hello"}
```

this happens:

---

## Step 1: `app.get("/")` Runs First

`app.get("/")` is actually a method call.

It returns a decorator function.

Equivalent:

```python
decorator = app.get("/")
```

---

## Step 2: Decorator Receives `home`

Then Python passes the function into the decorator.

Equivalent:

```python
decorator(home)
```

---

# 5. What Does the Decorator Do?

The decorator DOES NOT call `home()`.

Instead, it STORES the function inside FastAPI routing tables.

Internally something like:

```python
app.routes.append({
    "path": "/",
    "method": "GET",
    "handler": home
})
```

So FastAPI remembers:

| URL | Method | Function |
| --- | ------ | -------- |
| `/` | GET    | `home`   |

The function is only REGISTERED.

Not executed.

---

# 6. Application Startup

Now Uvicorn starts the server.

Uvicorn is:

* An ASGI server
* Like a waiter between internet and FastAPI

It:

* Opens a network socket
* Starts listening for requests
* Waits forever

Example:

```text
Browser ---> Uvicorn ---> FastAPI
```

---

# 7. What is ASGI?

ASGI = Asynchronous Server Gateway Interface

It is a communication protocol between:

* Web server (Uvicorn)
* Python web app (FastAPI)

Think:

```text
HTTP Request
    ↓
Uvicorn
    ↓ ASGI
FastAPI
```

ASGI defines HOW requests are passed.

---

# 8. Server Starts Listening

Uvicorn now listens on:

```text
http://127.0.0.1:8000
```

Nothing happens until a client sends a request.

---

# 9. Browser Sends Request

Suppose browser visits:

```text
http://127.0.0.1:8000/
```

Browser sends HTTP request:

```http
GET / HTTP/1.1
Host: 127.0.0.1
```

---

# 10. Who Receives the Request First?

Uvicorn receives it first.

NOT FastAPI.

Important.

```text
Browser
   ↓
Uvicorn
```

---

# 11. Uvicorn Converts Request Into ASGI Format

Uvicorn transforms HTTP request into ASGI scope.

Something like:

```python
scope = {
    "type": "http",
    "method": "GET",
    "path": "/"
}
```

---

# 12. Uvicorn Calls FastAPI App

THIS is the key moment.

Uvicorn literally CALLS the FastAPI app object.

Conceptually:

```python
await app(scope, receive, send)
```

This is why FastAPI app is called an ASGI application.

The app object itself is callable.

---

# 13. FastAPI Starts Processing

FastAPI now receives:

* URL path
* HTTP method
* Headers
* Body
* Query params

Now FastAPI must decide:

> Which function should handle this request?

---

# 14. Route Matching Happens

FastAPI checks registered routes.

Remember earlier?

```python
@app.get("/")
def home():
```

stored route info.

FastAPI searches:

| Request Path | Registered Path |
| ------------ | --------------- |
| `/`          | `/`             |

Match found.

---

# 15. FastAPI Chooses the Function

Now FastAPI knows:

```python
home()
```

should handle this request.

BUT before calling it, many things may happen.

---

# 16. Middleware Runs First

If middleware exists:

```python
@app.middleware("http")
async def middleware(request, call_next):
```

middleware executes BEFORE route function.

Flow:

```text
Request
   ↓
Middleware
   ↓
Route Function
   ↓
Middleware
   ↓
Response
```

Middleware can:

* Log requests
* Check authentication
* Modify response
* Measure timing

---

# 17. Dependency Injection Happens

If route has dependencies:

```python
@app.get("/")
def home(user=Depends(get_user)):
```

FastAPI first calls:

```python
get_user()
```

before `home()`.

This is automatic dependency injection.

---

# 18. Request Validation Happens

Suppose:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

FastAPI uses Pydantic to validate incoming JSON.

If invalid:

```json
{
  "name": "Ashfak",
  "age": "hello"
}
```

FastAPI automatically returns error.

Your function never runs.

---

# 19. Finally Your Function is Called

NOW FastAPI finally executes:

```python
home()
```

This is the moment beginners usually imagine happens earlier.

But many internal steps happen before this.

---

# 20. Your Function Returns Data

Example:

```python
return {"message": "Hello"}
```

Python dictionary returned.

---

# 21. FastAPI Converts Data to JSON

FastAPI automatically serializes:

```python
{"message": "Hello"}
```

into:

```json
{"message":"Hello"}
```

---

# 22. Response Object Created

FastAPI creates HTTP response:

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

with JSON body.

---

# 23. Response Goes Back to Uvicorn

Flow:

```text
home()
   ↓
FastAPI
   ↓
Uvicorn
```

---

# 24. Uvicorn Sends Data Through Socket

Uvicorn writes bytes into network socket.

Internet sends response to browser.

---

# 25. Browser Receives Response

Browser shows:

```json
{"message":"Hello"}
```

Done.

---

# FULL REQUEST FLOW

```text
Browser
   ↓
TCP Connection
   ↓
Uvicorn Server
   ↓
ASGI Call
   ↓
FastAPI App
   ↓
Middleware
   ↓
Dependency Injection
   ↓
Validation
   ↓
Route Matching
   ↓
Your Function
   ↓
Response Serialization
   ↓
Uvicorn
   ↓
Browser
```

---

# 26. What About `async def`?

Example:

```python
@app.get("/")
async def home():
```

Now FastAPI can pause while waiting.

Useful for:

* Database queries
* APIs
* File operations

This allows concurrency.

Uvicorn uses an event loop (`asyncio`) to manage many requests simultaneously.

---

# 27. Auto Reload (`--reload`)

In development mode:

```bash
fastapi dev main.py
```

FastAPI watches files.

When file changes:

1. Old server process stops
2. Python re-imports files
3. Routes register again
4. New server starts

That’s why edits instantly apply.

---

# 28. Startup Events

Example:

```python
@app.on_event("startup")
async def startup():
    print("Starting")
```

Executed when app starts.

Useful for:

* DB connection
* Cache initialization
* ML model loading

---

# 29. Shutdown Events

Example:

```python
@app.on_event("shutdown")
async def shutdown():
    print("Stopping")
```

Executed before server exits.

Useful for:

* Closing DB
* Cleaning resources
* Saving data

---

# 30. Important Mental Model

This is the MOST important thing to understand:

Your FastAPI app is mostly:

## A giant routing + request-processing machine

Your functions are NOT running automatically.

They are:

1. Registered earlier
2. Stored internally
3. Selected later during request handling
4. Called dynamically by FastAPI

---

# WHO CALLS YOUR `@app.get()` FUNCTION?

This is the exact chain:

```text
Browser Request
   ↓
Uvicorn receives request
   ↓
Uvicorn calls FastAPI ASGI app
   ↓
FastAPI route matcher finds endpoint
   ↓
FastAPI internally calls your function
```

So:

> FastAPI calls your function dynamically after matching the route.

Not Python automatically.

Not the decorator itself.

Not Uvicorn directly.

FastAPI does it.

---

# Internal Simplified Pseudo Code

Very simplified idea:

```python
routes = {
    ("/", "GET"): home
}

def handle_request(path, method):
    func = routes[(path, method)]
    return func()
```

That’s the core idea behind routing.

---

# One More Important Thing

FastAPI itself is built on:

* FastAPI
* Starlette
* Pydantic
* Uvicorn
* Python `asyncio`

FastAPI mainly adds:

* Automatic validation
* Dependency injection
* OpenAPI docs
* Type-based parsing
* Developer experience

Starlette handles most ASGI/web internals.

---

# Simple Real-World Analogy

```text
Browser = Customer
Uvicorn = Receptionist
FastAPI = Manager
Routes = Department map
Your function = Worker
```

Customer arrives:

1. Receptionist receives customer
2. Sends to manager
3. Manager checks department map
4. Correct worker chosen
5. Worker produces result
6. Result returned to customer

---

# Final Core Understanding

The lifecycle is:

```text
Code Import
    ↓
Routes Registered
    ↓
Server Starts
    ↓
Wait for Requests
    ↓
Request Arrives
    ↓
Route Matching
    ↓
Middleware
    ↓
Dependencies
    ↓
Validation
    ↓
Your Function Called
    ↓
Response Generated
    ↓
Response Sent Back
```
