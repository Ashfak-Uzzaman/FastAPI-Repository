**Jinja2** is a powerful, fast, and designer-friendly **templating engine** written in Python and runs on Python 3.7+. It is widely used for generating dynamic HTML (in web frameworks like Flask and Django alternatives), configuration files, XML, emails, and any text-based output.

### What is Jinja2?
- **Full-featured templating language** inspired by Django templates but more flexible and extensible.
- 
- Secure by default (auto-escaping to prevent XSS).
- Highly performant and used in production by many large applications.

### Core Syntax

#### 1. **Expressions / Output Variables**
```jinja
{{ variable }}
{{ user.name }}
{{ 5 + 10 }}
{{ article.title|title }}   <!-- with filter -->
```

#### 2. **Control Structures** (Statements)
Use `{% %}` for logic:

```jinja
{% if user.is_active %}
    <p>Welcome back, {{ user.name }}!</p>
{% elif user.is_guest %}
    <p>Please log in.</p>
{% else %}
    <p>Access denied.</p>
{% endif %}

{% for item in items %}
    <li>{{ item.name }} - {{ item.price }}</li>
{% else %}
    <p>No items found.</p>
{% endfor %}
```

#### 3. **Filters** (Pipes)
Modify variables on the fly:
```jinja
{{ name|upper }}
{{ text|truncate(100) }}
{{ price|float|format('%.2f') }}
{{ date|format_datetime('short') }}
```

#### 4. **Template Inheritance**
```jinja
<!-- base.html -->
<!DOCTYPE html>
<html>
<head><title>{% block title %}My Site{% endblock %}</title></head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- child.html -->
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <h1>Hello World</h1>
{% endblock %}
```

#### 5. **Includes & Macros**
```jinja
{% include "header.html" %}

{% macro input(name, type='text') %}
    <input type="{{ type }}" name="{{ name }}">
{% endmacro %}

{{ input('email', 'email') }}
```

### Common Features
- **Auto-escaping** (enabled by default in HTML context)
- **Template blocks**, loops, conditionals
- **Whitespace control** (`{%- -%}` and `{{- -}}`)
- **Custom filters, tests, and globals**
- **Sandbox mode** for untrusted templates
- **i18n** support (internationalization)

***Example:***

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.html')
output = template.render(user=user, items=items)
```
