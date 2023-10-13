def print_finish_message(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print(f'Finish {func.__name__} SUCCESSFULLY!')
    return wrapper
