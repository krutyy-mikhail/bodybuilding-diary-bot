from dao import dao


class UserService:
    dao = dao.UserDAO()

    def create(self, user):
        self.dao.create(user)

    def get(self, user_id):
        return self.dao.get_user_by_id(user_id)


class FoodReportService:
    dao = dao.FoodReportDAO()


class BodyReportService:
    dao = dao.BodyReportDAO()


class NormalFoodService:
    dao = dao.NormalFoodDAO()
