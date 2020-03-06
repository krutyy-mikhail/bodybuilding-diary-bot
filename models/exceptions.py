class BaseValidationFieldError(ValueError):
    pass


class NotPozitiveIdFieldError(BaseValidationFieldError):
    pass


class NotPozitiveFloatFieldError(BaseValidationFieldError):
    pass


class FieldIsTooLong(BaseValidationFieldError):
    pass


class FieldNotMatchPattern(BaseValidationFieldError):
    pass
