from models import fields
from dao import dao


class Model:
    id = fields.IdField(is_blank=True)

    def __init__(self, *args, **kwargs):
        if args:
            raise TypeError('Constructor takes only keyword arguments.')

        self.id = None

        for attribute, value in vars(type(self)).items():
            if attribute.startswith('__') or callable(value):
                continue

            if value.is_blank:
                setattr(self, attribute, None)
            else:
                setattr(self, attribute, value._default)

        for attribute, value in kwargs.items():
            if attribute in vars(type(self)) or attribute == 'id':
                setattr(self, attribute, value)
            else:
                raise TypeError('Incorrect attribute {}.'.format(
                    attribute))


class User(Model):
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    phone = fields.PhoneField(max_length=50, is_blank=True)
    email = fields.EmailField(max_length=50, is_blank=True)
    is_admin = fields.BoleanField(is_blank=True)


class FoodReport(Model):
    fats = fields.PositiveFloatField()
    carbohydrates = fields.PositiveFloatField()
    calories = fields.PositiveFloatField()
    cellulose = fields.PositiveFloatField()
    date_report = fields.DateTimeField(is_blank=True)
    user_id = fields.IdField()


class BodyReport(Model):
    weight = fields.PositiveFloatField()
    size_waist = fields.PositiveFloatField()
    size_chest = fields.PositiveFloatField()
    size_thighs = fields.PositiveFloatField()
    size_left_biceps = fields.PositiveFloatField()
    size_right_biceps = fields.PositiveFloatField()
    size_pelvis = fields.PositiveFloatField()
    size_buttocks = fields.PositiveFloatField()
    date_report = fields.DateTimeField(is_blank=True)
    user_id = fields.IdField()


class NormalFood(Model):
    normal_fats = fields.PositiveFloatField()
    normal_carbohydrates = fields.PositiveFloatField()
    normal_calories = fields.PositiveFloatField()
    normal_cellulose = fields.PositiveFloatField()
    user_id = fields.IdField()
