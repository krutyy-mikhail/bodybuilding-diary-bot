def is_null(method):
    def decorator(self, instance, value):
        if self.is_blank and value is None:
            instance.__dict__[self.name] = value
        else:
            method(self, instance, value)
    return decorator
