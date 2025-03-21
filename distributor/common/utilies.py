class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        elif args or kwargs:
            raise Exception(f"Singleton {cls.__name__} was already initialized")
        return cls._instances[cls]