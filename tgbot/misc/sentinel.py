def allow_access(state: bool):
    def decorator(func):
        setattr(func, "allow", state)
        return func

    return decorator
