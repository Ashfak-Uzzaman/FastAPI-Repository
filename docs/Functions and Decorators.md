# 1. First understand: functions are objects in Python

In Python, functions can be:

* stored in variables
* passed as arguments
* returned from another function

Example:

```python
def greet():
    print("Hello")

x = greet

x()
```

Output:

```python
Hello
```

Notice:

* `x = greet` does NOT call the function
* it stores the function itself

So functions behave like objects.

This is the foundation of decorators.

---

# 2. What is `@` in decorators?  

## What is a Decorator?

A decorator is a way to **modify or extend the behavior of a function (or class)** without changing its original code.  

A **decorator** is a function that:

1. **Takes** another function (or class) as input
2. **Wraps** or extends its behavior
3. **Returns** a new function (or the modified original)

*In Python, the `@` symbol is often used for **decorators**.*

When you write:

```python
@myDecorator
def hello():
    print("Hello")
```

Python internally does this:

```python
def hello():
    print("Hello")

hello = myDecorator(hello)
```

So:

```python
@something
```

means:

> “Take the function below and pass it into `something`.”

---

# 3. Simple decorator example

Let's build one slowly.

---

## Step 1: Original function

```python
def sayHello():
    print("Hello")
```

Calling:

```python
sayHello()
```

Output:

```python
Hello
```

---

## Step 2: Create a decorator

```python
def myDecorator(func):

    def insideDecorator():
        print("Before function")

        func()

        print("After function")

    return insideDecorator
```

Now apply it manually:

```python
sayHello = myDecorator(sayHello)

sayHello()
```

Output:

```python
Before function
Hello
After function
```

---

# 4. What happened internally?

This line:

```python
sayHello = myDecorator(sayHello)
```

does this:

* passes `sayHello` function into `myDecorator`
* `func` receives it
* `insideDecorator` is returned
* `sayHello` now becomes `insideDecorator`

So now:

```python
sayHello()
```

actually calls:

```python
insideDecorator()
```

which then calls the original function.

---

# 5. Same thing using `@`

Instead of writing:

```python
sayHello = myDecorator(sayHello)
```

we can write:

```python
@myDecorator
def sayHello():
    print("Hello")
```

Full code:

```python
def myDecorator(func):

    def insideDecorator():
        print("Before function")

        func()

        print("After function")

    return insideDecorator


@myDecorator
def sayHello():
    print("Hello")


sayHello()
```

Output:

```python
Before function
Hello
After function
```

So `@myDecorator` is just cleaner syntax.

---

# 6. Decorator with parameters

Now suppose the function has arguments.

---

## Without decorator

```python
def add(a, b):
    print(a + b)

add(3, 5)
```

Output:

```python
8
```

---

## Decorator version

```python
def myDecorator(func):

    def insideDecorator(a, b):
        print("Numbers received:", a, b)

        func(a, b)

        print("Function finished")

    return insideDecorator


@myDecorator
def add(a, b):
    print(a + b)


add(3, 5)
```

Output:

```python
Numbers received: 3 5
8
Function finished
```

---

# 7. More flexible version using `*args` and `**kwargs`

A decorator usually does not know:

* how many arguments
* positional or keyword arguments

So decorators often use:

```python
*args
**kwargs
```

Example:

```python
def myDecorator(func):

    def insideDecorator(*args, **kwargs):

        print("Before function")

        result = func(*args, **kwargs)

        print("After function")

        return result

    return insideDecorator


@myDecorator
def multiply(a, b):
    return a * b


x = multiply(4, 5)

print(x)
```

Output:

```python
Before function
After function
20
```

---

# 8. Real-life analogy

Think of a decorator like wrapping a gift box.

Original function:

```text
Gift
```

Decorator adds extra behavior:

```text
Wrapper + Gift + Ribbon
```

But the original gift stays unchanged.

---

# 9. Common real uses of decorators

Decorators are heavily used for:

* logging
* authentication
* timing execution
* caching
* permissions
* route handling in web frameworks

Example idea:

```python
@loginRequired
def dashboard():
    ...
```

or

```python
@timer
def heavyCalculation():
    ...
```

---

# 10. Visual flow of decorator

Suppose:

```python
@myDecorator
def hello():
    print("Hello")
```

Internally:

```text
hello function
      ↓
passed into myDecorator
      ↓
returns insideDecorator
      ↓
hello now points to insideDecorator
```

Then:

```python
hello()
```

actually becomes:

```python
insideDecorator()
```

which may call original `hello()` inside it.

---

# 11. Important idea

Decorator usually:

1. receives a function
2. creates another function
3. adds extra behavior
4. returns the new function

Pattern:

```python
def decorator(func):

    def wrapper():
        # extra work

        func()

        # extra work

    return wrapper
```

---

# 12. Very important detail

This:

```python
func
```

means:

> function object

But this:

```python
func()
```

means:

> execute/call the function

Huge difference.

---

## One more nice example

```python
def smartDivide(func):

    def wrapper(a, b):

        if b == 0:
            print("Cannot divide by zero")
            return

        return func(a, b)

    return wrapper


@smartDivide
def divide(a, b):
    print(a / b)


divide(10, 2)

divide(10, 0)
```

Output:

```python
5.0
Cannot divide by zero
```

Decorator added safety without changing original `divide()` logic.

---

# 13. Stacking Multiple Decorators

You can apply multiple decorators to a single function. They are applied **bottom-up**:

```python
@decorator_one
@decorator_two
def my_func():
    pass

# Equivalent to:
my_func = decorator_one(decorator_two(my_func))
```

---

# 14. Decorators That Accept Parameters

To make a decorator that itself takes arguments, you add one more layer of nesting:

```python
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("Hello!")

hello()
```

**Output:**
```
Hello!
Hello!
Hello!
```

---

# 15. Decorators with arguments and  inside class decorator

```python
class MyDecorator:

    def message(text):

        def actualDecoratorFunction(func):

            def wrapperFunction():
                print("Message:", text)

                func()

            return wrapperFunction

        return actualDecoratorFunction



# message() must return a decorator function and that decorator function receives the decorated function (here 'hello') as a parameter.

@MyDecorator.message("Welcome!") # This 'message()' function have to return the function that takes a function (here 'hello()')  as a parameter.
def hello():
    print("Hello")


hello()
```

Here, this: 

```python
@MyDecorator.message("Welcome!")
def hello():
    print("Hello")
```

is internally equivalent to and becomes this:

```python
hello = MyDecorator.message("Welcome!")(hello)
```

Now calling `hello()`:

```python
hello()
```

Output:

```python
Message: Welcome!
Hello
```

---

# Expanded version (very clear)

Here is the same thing broken into smaller steps:

```python
class MyDecorator:

    def message(text):

        def actualDecoratorFunction(func):

            def wrapperFunction():
                print("Message:", text)

                func()

            return wrapperFunction

        return actualDecoratorFunction


def hello():
    print("Hello")


# Step 1
actualDecoratorFunction = MyDecorator.message("Welcome!")

# Step 2
wrapperFunction = actualDecoratorFunction(hello)

wrapperFunction()

''' Output:
Message: Welcome!
Hello
'''

# Step 3
hello = wrapperFunction # we are containing/saving the "wrapperFunction()" (step-2) in "hello". Now "hello" is a function - hello()

hello() # This actually the "wrapperFunction()" of step-2. It exactly do the same task

''' O/P:
Message: Welcome!
Hello
```

---

# 16. Simple decorator (without arguments) VS Decorator with arguments

### Simple decorators without arguments

Example:

```python
@myDecorator
def hello():
```

Internally:

```python
hello = myDecorator(hello)
```

Here:

* `myDecorator` itself directly receives the function
* no extra returned decorator is needed

So:

| Syntax            | What happens           |
| ----------------- | ---------------------- |
| `@decorator`      | `decorator(func)`      |
| `@decorator(...)` | `decorator(...)(func)` |

This is a VERY important distinction.

---

## ***Very important pattern***

## Simple decorator

```python
@decorator
```

Structure:

```python
def decorator(func):
```
## Decorator with arguments

```python
@decorator(argument)
```

Structure:

```python
def decorator(argument):

    def actualDecorator(func):
```

That extra layer exists because:

* first call handles decorator arguments
* second call handles the function being decorated

---

# 17. Function with multiple decorators

When a function has multiple decorators, they are applied **from the bottom up** (the decorator closest to the function runs first).

Example:

```python
def deco1(func):
    def wrapper():
        print("deco1 before")
        func()
        print("deco1 after")
    return wrapper

def deco2(func):
    def wrapper():
        print("deco2 before")
        func()
        print("deco2 after")
    return wrapper

@deco1
@deco2
def greet():
    print("Hello")
```

This is equivalent to:

```python
greet = deco1(deco2(greet))
```

So the execution order becomes:
Output:

```text
deco1 before
deco2 before
Hello
deco2 after
deco1 after
```
---
Here,

```python
def deco1(func):
    def wrapper():
        print("deco1 before")
        func()
        print("deco1 after")
    return wrapper

def deco2(func):
    def wrapper():
        print("deco2 before")
        func()
        print("deco2 after")
    return wrapper

@deco1
@deco2
def greet():
    print("Hello")
```
is exactly equal to:

```python
def greet():
    print("Hello")

wrapper2 = deco2(greet)

wrapper1 = deco1(wrapper2)

greet = wrapper1
```

More extention:

```python
wrapper2 = deco2(greet)
wrapper2()
''' Output:
deco2 before
Hello
deco2 after
'''

wrapper1 = deco1(wrapper2)
wrapper1()
''' Output:
deco1 before
deco2 before
Hello
deco2 after
deco1 after
'''

greet = wrapper1
```

Key points:

* The **bottom decorator is applied first**.
* The **top decorator wraps the result** of the lower one.
* Decorators stack like nested functions.

---

# 18. Using `functools.wraps`

`@functools.wraps` is a helper used **inside decorators**.

Its job is to preserve information about the original function when it gets wrapped by a decorator.

Without it, Python forgets details about the original function.

---

### 18.1 Problem without `@wraps`

Look carefully.

```python
def myDecorator(func):

    def wrapper():
        print("Before function")
        func()

    return wrapper


@myDecorator
def sayHello():
    """This function prints hello"""
    print("Hello")
```

Now check:

```python
print(sayHello.__name__)
print(sayHello.__doc__)
```

Output:

```python
wrapper
None
```

Problem:

* original name `sayHello` is lost
* docstring is lost

Because:

```python
sayHello = myDecorator(sayHello)
```

And `myDecorator` returned `wrapper`.

So now `sayHello` actually points to `wrapper`.

---

### 18.2 Solution: `functools.wraps`

Python provides:

```python
from functools import wraps
```

Now:

```python
from functools import wraps

def myDecorator(func):

    @wraps(func)
    def wrapper():
        print("Before function")
        func()

    return wrapper


@myDecorator
def sayHello():
    """This function prints hello"""
    print("Hello")
```

Now:

```python
print(sayHello.__name__)
print(sayHello.__doc__)
```

Output:

```python
sayHello
This function prints hello
```

*Now original metadata is preserved.*

---

> **Best Practice:** Always use `@functools.wraps` inside your decorator wrappers.

---

# 19. Built-in Python Decorators

Python ships with several commonly used decorators:

| Decorator | Where Used | Purpose |
|---|---|---|
| `@staticmethod` | Inside a class | Defines a method that doesn't take `self` or `cls` |
| `@classmethod` | Inside a class | Defines a method that takes `cls` instead of `self` |
| `@property` | Inside a class | Makes a method accessible like an attribute |
| `@abstractmethod` | Inside an abstract class | Forces subclasses to implement the method |
| `@functools.lru_cache` | Any function | Caches return values for repeated inputs |

### Example: `@property`

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14159 * self.radius ** 2

c = Circle(5)
print(c.area)   # Called like an attribute, not c.area()
```

---

# 20. Summary

Decorator:

* takes a function
* modifies/enhances behavior
* returns another function

`@decoratorName` is just shorthand for:

```python
functionName = decoratorName(functionName)
```

Most common structure:

```python
def decorator(func):

    def wrapper(*args, **kwargs):

        # extra work

        result = func(*args, **kwargs)

        # extra work

        return result

    return wrapper
```

## ***Very important pattern***

## Simple decorator

```python
@decorator
```

Structure:

```python
def decorator(func):
```

---

## Decorator with arguments

```python
@decorator(argument)
```

Structure:

```python
def decorator(argument):

    def actualDecorator(func):
```