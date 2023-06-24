def dec(func):
    def run(*args, **kwargs):
        print(*args)
        print(*list(i for i in args))
        return func

    return run