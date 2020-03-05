import re
from datetime import datetime

from decorators import is_null
from models import exceptions


class AbstractField:
    def __init__(self, is_blank=False):
        self.is_blank = is_blank

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

    def _check_type(self, value):
        if not isinstance(value, self._type):
            error = 'Attribute "{}" must be type of "{}".'.format(
                self.name, self._type.__name__)
            raise TypeError(error)


class IdField(AbstractField):
    _type = int

    @is_null
    def __set__(self, instance, value):
        self._check_type(value)
        self._check_positive_integer(value)
        super().__set__(instance, value)

    def _check_positive_integer(self, value):
        if value < 1:
            error = 'Attribute "{}" must be grater and equal 1.'.format(
                self.name)
            raise exceptions.NotPozitiveIdFieldError(error)


class PositiveFloatField(AbstractField):
    _type = float
    _default = 0.0

    @is_null
    def __set__(self, instance, value):
        super()._check_type(value)
        self._check_positive_float(value)
        super().__set__(instance, value)

    def _check_positive_float(self, value):
        if value < 0.0:
                error = 'Attribute "{}" must be positive.'.format(
                    self.name)
                raise exceptions.NotPozitiveFloatFieldError(error)


class CharField(AbstractField):
    _type = str
    _default = ''
    _pattern = r'[\w]*'

    def __init__(self, max_length, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = max_length

    @is_null
    def __set__(self, instance, value):
        self._check_type(value)
        self._check_length(value)
        self._check_pattern(value)

        super().__set__(instance, value)

    def _check_length(self, value):
        max_length = self.max_length
        if len(value) > max_length:
            error = '''Length of attribute "{}" must be less or equal
                     {}.'''.format(self.name, max_length)
            raise exceptions.FieldIsTooLong(error)

    def _check_pattern(self, value):
        if not re.fullmatch(self._pattern, value):
            error = 'Attribute "{}" incorrect.'.format(self.name)
            raise exceptions.FieldNotMatchPattern(error)


class PhoneField(CharField, AbstractField):
    _pattern = r'\+?[7,8]?[\d]{10}'
    _default = '89991234567'

    @is_null
    def __set__(self, instance, value):
        super().__set__(instance, value)
        super(CharField, self).__set__(instance, value)


class EmailField(CharField, AbstractField):
    _pattern = r'[\d,\w]+@\w+\.\w+'
    _default = 'example@example.com'

    @is_null
    def __set__(self, instance, value):
        super().__set__(instance, value)
        super(CharField, self).__set__(instance, value)


class DateTimeField(AbstractField):
    _type = datetime
    _default = datetime.now()

    @is_null
    def __set__(self, instance, value):
        self._check_type(value)
        super().__set__(instance, value)


class BoleanField(AbstractField):
    _type = bool
    _default = False

    @is_null
    def __set__(self, instance, value):
        self._check_type(value)
        super().__set__(instance, value)
