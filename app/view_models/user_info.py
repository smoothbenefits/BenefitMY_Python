from app.models.person import SELF
from .person_info import PersonInfo


class UserInfo(object):
    first_name = ''
    last_name = ''
    person_info = None

    def __init__(self, user_model):
        person_model = user_model.family.filter(relationship=SELF).first()
        if (person_model):
            self.person_info = PersonInfo(person_model)

        if (self.person_info):
            self.first_name = self.person_info.first_name
            self.last_name = self.person_info.last_name
        else:
            self.first_name = user_model.first_name
            self.last_name = user_model.last_name

    @property
    def full_name(self):
        if self.first_name is not None and self.last_name is not None:
            return self.first_name + ' ' + self.last_name
        return None
