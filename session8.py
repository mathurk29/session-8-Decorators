from functools import wraps
from datetime import datetime
from time import perf_counter

# Decorator that allows to run a function only at odd seconds, else prints out "We're even!"


def odd_it(fn):
    ''' Decorator that allows to run a function only at odd seconds, else prints out \"We're even!\" '''
    # MISSING CODE
    from datetime import datetime, timezone
    run_second = datetime.now(timezone.utc).second
    from functools import wraps

    @wraps(fn)
    def inner(*args, **kwargs):
        if run_second % 2 == 0:
            print("We are even")
        else:
            return fn(*args, **kwargs)
    return inner

# The same logger that we coded in the class
# it will be tested against a function that will be sent 2 parameters, and
# it would return some random string.


def logger(fn):
    '''Decorator for logging. It prints:
    1. function name
    2. Execution time
    3. Function description
    4. Docstring
    5. Functional Annotations
    '''
    from functools import wraps
    from datetime import datetime, timezone
    from time import perf_counter

    @wraps(fn)
    def inner(*args, **kwargs):
        run_dt = datetime.now(timezone.utc)
        start = perf_counter()
        result = fn(*args, **kwargs)
        end = perf_counter()
        print(f'The function_name {fn.__name__}: called at{run_dt}')
        print(f'Execution time {end - start}')
        print(f'Function description is {inner.__doc__}')
        print(f'This is a function\'s writeup: {inner.__doc__}')
        print(f'Function annotation: {inner.__annotations__}')
        return result
    return inner


# start with a decorator_factory that takes an argument one of these strings,
# high, mid, low or no
# then write the decorator that has 4 free variables
# based on the argument set by the factory call, give access to 4, 3, 2 or 1 arguments
# to the function being decorated from var1, var2, var3, var4
# YOU CAN ONLY REPLACE "#potentially missing code" LINES WITH MULTIPLE LINES BELOW
# KEEP THE REST OF THE CODE SAME
def decorator_factory(access: str):
    ''' Decorator factory to set the accesss level and accordingly return the list of allowed variables.'''
    def dec(fn):
        var1 = ''
        var2 = ''
        var3 = ''
        var4 = ''
        from functools import wraps

        @wraps(fn)
        def inner(*args, **kwarags):
            nonlocal var1, var2, var3, var4
            if access == 'high':
                return [var1, var2, var3, var4]
            elif access == 'mid':
                return [var1, var2, var3]
            elif access == 'low':
                return [var1, var2]
            elif access == 'no':
                return [var1]
            else:
                return "Improper access keyword set"
        return inner
    return dec


# The authenticate function. Start with a dec_factory that sets the password. It's inner
# will not be called with "password", *args, **kwargs on the fn
def authenticate(set_password):
    def dec(fn):
        def inner(given_password):
            if given_password == set_password:
                result = fn()
            else:
                result = "Wrong Password"
            return result
        return inner
    return dec


# The timing function
def timed(reps):
    ''' Decorator factory which sets the number of times the function is called to find average execution time.'''
    def dec(fn):
        from time import perf_counter
        from functools import wraps

        @wraps(fn)
        def inner(*args, **kwargs):
            total_elapsed = 0
            for _ in range(reps):
                start = perf_counter()
                result = fn(*args, **kwargs)
                end = perf_counter()
                total_elapsed += end - start
            avg_elapsed = total_elapsed / reps
            print(f'Avg run time for {reps} times: {avg_elapsed}')
            return result
        return inner

    return dec
