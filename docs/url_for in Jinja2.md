# **`url_for()` Syntax in FastAPI Jinja2**

---

## 1. Basic Route URL

```html
{{ url_for('route_name') }}
```

Generates URL for a route.

Example:

```html
{{ url_for('about') }}
```

Result:

```text
/about
```

---

## 2. Route with Path Parameter

```html
{{ url_for('route_name', parameter=value) }}
```

Example:

```html
{{ url_for('profile', id=5) }}
```

Result:

```text
/user/5
```

---

## 3. Multiple Parameters

```html
{{ url_for('route_name', param1=value1, param2=value2) }}
```

Example:

```html
{{ url_for('post', category='python', id=10) }}
```

Result:

```text
/post/python/10
```

---

## 4. Static Files

```html
{{ url_for('static', path='filename') }}
```

Example:

```html
{{ url_for('static', path='style.css') }}
```

Result:

```text
/static/style.css
```

---

## 5. Static File Inside Folder

```html
{{ url_for('static', path='folder/file.css') }}
```

Example:

```html
{{ url_for('static', path='css/main.css') }}
```

Result:

```text
/static/css/main.css
```

---

## 6. Custom Route Name

### Route

```python
@app.get("/about", name="about_page")
```

### Template

```html
{{ url_for('about_page') }}
```

---

| Code         | url_for name                |
| ------------ | --------------------------- |
| No `name=`   | function name (`get_about`) |
| With `name=` | custom name (`about_page`)  |

### 6.1. Without `name=...`

```python
@app.get("/about")
def get_about():
    pass
```

Here:

* Route path = `"/about"`
* Function name = `"get_about"`
* Route name = `"get_about"` ← automatically taken from function name

So:

```html
{{ url_for('about') }}
```

works.

---

### 6.2. With `name=...`

```python
@app.get("/about", name="about_page")
def get_about():
    pass
```

Now:

* Route path = `"/about"`
* Function name = `"get_about"`
* Route name = `"about_page"` ← custom name overrides function name

So now:

```html
{{ url_for('about_page') }}
```

works.

BUT:

```html
{{ url_for('about') }}
```

will NOT work anymore.

***Because FastAPI now registered the route using***:

```text
about_page
```

NOT:

```text
about
```

---

## 7. Python Side Syntax

```python
request.url_for("route_name")
```

Example:

```python
request.url_for("about")
```

Result:

```text
http://127.0.0.1:8000/about
```

---

## 8. Python Side with Parameters

```python
request.url_for("route_name", parameter=value)
```

Example:

```python
request.url_for("profile", id=5)
```

---

## 9. Required Template Context

```python
{"request": request}
```

Needed for `url_for()` to work inside Jinja2 templates.
