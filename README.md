> Author: *Kshitij Mathur*

> Email Id: *mathurk29@gmail.com*

# <center> EPAi Session 8 - Decorators  <center>

## Closures vs Decorators

Decorators are nothing but the function which **<u>returned</u>** the closure!!

```python
def counter(fn):
    count = 0

    def inner(*args **kwargs):
        nonlocal count
        count += 1
        print(f'Function {fn.__name__} was called {count} times')
        return fn(*args **kwargs)
    return inner
```

Recall that ```inner()``` along with its freevars ```count``` together is called Closure.

Now the funtion ```counter``` itself is called **Decorator**.

We can use two syntaxes to apply closure to a function:

```python
# Using Closure Syntax:
def add(a b = 0):
    return a + b

add = counter(add)
```

```python
# Using Decorators:
@counter
def add(a b = 0):
    return a + b
```

This session we will learn about the Decorator Syntax. 

In general a decorator function: 
- takes a function as an argument 
- returns a closure 
- the closure usually accepts any combination of parameters 
- runs some code in the inner function (closure) 
- the closure function calls the original function using the arguments passed to the closure 
- returns whatever is returned by that function call 

Here add is called to be decorated with the decorator counter.

<br>

# The *@wrap* Decorator

An issue which we face in using Decorators is that since the decorated function is assigned equal to closure - all of its functional introspection is replace with that of the closure. See this:


```python
> add.__name__
'inner'

> help(add)
Help on function inner in module __main__: inner(*args **kwargs)

> print(inspect.getsource(add))
def inner(*args **kwargs):
    nonlocal count
    count += 1
    print(f'Function {fn.__name__} was called {count} times')
    return fn(*args **kwargs)

>inspect.signature(add)
<Signature (*args **kwargs)>

> inspect.signature(add).parameters
mappingproxy({'args': <Parameter *args> 'kwargs': <Parameter **kwargs>})

```

Fortunately there is a way to avoid this. Python provides a **decorator** to decorate the **inner** function inside ```functools```  called `wraps`

```python
from functools import wraps
def counter(fn):
    count = 0
    
    @wraps(fn)
    def inner(*args **kwargs):
        nonlocal count
        count += 1
        print({0} was called {1} times.format(fn.__name__ count))
    return inner

```

Notice `@wraps(fn)` decorator above `inner`.

Now introspecting we get:

```python
@counter
def add(a: int b: int=10) -> int:
    
    returns sum of two integers
    
    return a + b

> help(add)
Help on function add in module __main__:

add(a: int b: int = 10) -> int
    returns sum of two integers

> add.__name__
'add'

> print(inspect.getsource(add))
@counter
def add(a: int b: int=10) -> int:
    
    returns sum of two integers
    
    return a + b

```


# Decorator Examples 
## **1.** Timer :
<br>

```python
def timed(fn):
    from time import perf_counter
    from functools import wraps

    @wraps(fn)
    def inner(*args **kwargs):
        start = perf_counter()
        result = fn(*args **kwargs)
        end = perf_counter()
        elapsed = end - start

        args_ = [str(a) for a in args]
        kwargs_ = [f'{k} = {v}' for (k v) in kwargs.items()]
        all_args  = args_ + kwargs_
        args_str = ''.join(all_args)
        print(f'{fn.__name__}({args_str}) took {elapsed} to run.')
        return result
    return inner
```

The significance of above function is that now we have a utility in our hand to test the performance of any function just by adding a simple single line `@timed` before the definition of the function.

For ex:

```
@timed
> def add(a b):
     return a + b

> add(1 2)

add(12) took 8.299998626171146e-07 to run.

```

Note - if you want to add this decorator to a recursive function the decorator would be called for  for every recursive call.

```py
> @timed
  def calc_recursive_fib(n):
      if n < 2:
          return 1
  
      else: 
          return calc_recursive_fib(n - 1) + calc_recursive_fib(n - 2)

> calc_recursive_fib(6)


fib_recursed_2(10)
fib_recursed_2(1) took 7.099997674231417e-07 to run.
fib_recursed_2(0) took 9.300001693191007e-07 to run.
fib_recursed_2(2) took 0.0009001010002975818 to run.
fib_recursed_2(1) took 1.2850000075559365e-05 to run.
fib_recursed_2(3) took 0.008024188000035792 to run.
fib_recursed_2(1) took 5.800002327305265e-07 to run.
fib_recursed_2(0) took 7.799999366397969e-07 to run.
fib_recursed_2(2) took 0.0005001059998903656 to run.
fib_recursed_2(4) took 0.008904939000331069 to run.
fib_recursed_2(1) took 5.300003067532089e-07 to run.
fib_recursed_2(0) took 7.399999049084727e-07 to run.
fib_recursed_2(2) took 0.0003588839999792981 to run.
fib_recursed_2(1) took 6.999998731771484e-07 to run.
.
.
.
.
. #and so on
```
### To avoid this - simply wrap the recursive function inside another function!
<br>

```py
> @timed
 def fib_recursed(n):
     return calc_recursive_fib(n)

> fib_recursed(33)
fib_recursed(33) took 1.8473043710000638 to run.
```

## **2.** Logger


```python
def logger(fn):
    from functools import wraps
    from datetime import datetime timezone

    @wraps(fn)
    def inner(*args **kwargs):
        run_dt = datetime.now(timezone.utc)
        result = fn(*args **kwargs)
        print(f'{fn.__name__}: called {run_dt}')
        return result
    return inner
```

```python
@logger
def func_1():
    pass

> func_1()
func_1: called 2021-06-26 06:34:07.189183+00:00
```

### Note the sequence of how decorators and the decoratead are called

```python
def dec_1(fn):
    def inner():
        print('running dec_1')
        return fn()
    return inner
    
def dec_2(fn):
    def inner():
        print('running dec_2')
        return fn()
    return inner

@dec_1
@dec_2
def my_func():
    print('running my_func')

> my_func()
running dec_1
running dec_2
running my_func


```

# Memoization

The fancy term is nothing but the practise of saving the output of the recursions of a recursive function in a freevar(list/dict) of a decorated recursive function!


### Calculating Fibnocacci recursively:

```python
def fib(n):
    print ('Calculating fib({0})'.format(n))
    return 1 if n < 3 else fib(n-1) + fib(n-2)

### Note above that fib is same numbers is calculated repeatedly.
> fib(5)
Calculating fib(5)
Calculating fib(4)
Calculating fib(3)
Calculating fib(2)
Calculating fib(1)
Calculating fib(2)
Calculating fib(3)
Calculating fib(2)
Calculating fib(1)

```


### Using Class:

```python
class Fib:
    def __init__(self):
        self.cache = {1: 1 2: 1}
    
    def fib(self n):
        if n not in self.cache:
            print('Calculating fib({0})'.format(n))
            self.cache[n] = self.fib(n-1) + self.fib(n-2)
        return self.cache[n]

> f = Fib()
> f.fib(3)
Calculating fib(3)
2

# Notice fib(3) and is not calcualted now:
> f.fib(10)
Calculating fib(10)
Calculating fib(9)
Calculating fib(8)
Calculating fib(7)
Calculating fib(6)
Calculating fib(5)
Calculating fib(4)

```

The same class above can be written using Decorator: 
```python
# Memoization
def fib():
    cache = {1: 1 2: 2}
    
    def calc_fib(n):
        if n not in cache:
            print('Calculating fib({0})'.format(n))
            cache[n] = calc_fib(n-1) + calc_fib(n-2)
        return cache[n]
    
    return calc_fib

```

## A general Memoization function:

```python

def memoize_anything(fn):
    cache = dict()
    
    @wraps(fn)
    def inner(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    
    return inner
```

We have an in-built memoize decorator: `@lru_cache` from functools. Optional arg: maxsize.


# Decorator Factory

Till now we have seen that a decorator only takes one argument - the decorated fucntion. In fact, when we use pie symbol, we even did not need to provide that argument.

It has a implication - we cannot send additional freevar (or assign value to some freevar) to the closure of the decorator. This limitaiton needs to be overcome for certain use cases. 

> For ex: We need to set some variable value in the decorator.

Now - 

There is a way where we can  provide additional arguments to decorator - which can then be assigned to freevars of inner. 

We can to wrap it inside another function, which accepts some arguments. That function should return this decorator. This wrapper of decorator is called **Decorator Factory**

```python

def dec_factory(a, b):
    print('Got a call to decorator factory')
    def dec(fn):
        def inner(*args, **kwargs):
            print("running decotator inner")
            print('free variables I am getting from decorator call are: ', a, b)
            return fn(*args, **kwargs)
        return inner
    return dec

@dec_factory(10, 20)
def my_func(a, b):
    return a + b

Got a call to decorator factory
```

`my_func(2, 3)`

*running decotator inner*

<br>

# Session8.py

> ### `odd_it()`: A decorator that simply checks the time and run the decorated function only if it is odd > second.
> ### `logger()`: A decorator that is used to log name, exec time, docstring, and annotations of the decorated > function
> ### `decorator_factory()`: A decorator factory that sets the accesss level of a user and accordingly return > decorator which returns a list of allowed freevars.
> ### `authenticate()`: A decorator factory which sets the password for authenticating execution of a function.
> ### `timed()`: A decorator factory which sets the number of repeatitions of running a decorator and prints > the average time of the execution.