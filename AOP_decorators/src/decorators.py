def method_call_decorator(method):
    def inner(*args, **kwargs):
        print(f"Calling {method.__name__}({args[1:]}, {kwargs})")
        result = method(*args, **kwargs)
        print(f"Call to {method.__name__}({args[1:]}, {kwargs}) ended")
        return result
    return inner

def exception_catcher(method):
    def inner(*args, **kwargs):
        try:
            result = method(*args, **kwargs)
        except Exception as e:
            print(f"Caught exception '{e}' in call to {method.__name__}({args[1:]}, {kwargs})")
            return None
        else:
            return result
    return inner