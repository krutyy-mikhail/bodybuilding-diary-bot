from dao import dao


class AbstractService:
    _dao = None

    @property
    def dao(self):
        return self._dao

    @dao.setter
    def dao(self, value):
        class_ = type(self.dao)
        if not isinstance(value, class_):
            raise TypeError('Attribute "dao" must be object type of "{}".'.format(
                class_.__name__))
        self._dao = value


class UserService(AbstractService):
    _dao = dao.UserDAO()

    def create(self, user):
        self.dao.create(user)

    def get(self, user_id):
        return self.dao.get_user_by_id(user_id)


class FoodReportService(AbstractService):
    _dao = dao.FoodReportDAO()


class BodyReportService(AbstractService):
    _dao = dao.BodyReportDAO()


class NormalFoodService(AbstractService):
    _dao = dao.NormalFoodDAO()
