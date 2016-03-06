"""
models.py

App Engine datastore models

"""
import json

from google.appengine.ext import ndb


class ExampleModel(ndb.Model):
    """Example Model"""
    example_name = ndb.StringProperty(required=True)
    example_description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)


class UserModel(ndb.Model):
    name = ndb.StringProperty()
    gender = ndb.StringProperty()
    uuid = ndb.StringProperty()
    bluetooth = ndb.StringProperty()
    facebook_id = ndb.StringProperty()
    photo_url = ndb.StringProperty()
    facebook_token = ndb.StringProperty()
    features = ndb.StringProperty()
    weights = ndb.StringProperty()
    gps = ndb.StringProperty()
    where = ndb.StringProperty()
    locations = ndb.StringProperty()
    experience_education = ndb.StringProperty()
    experience_hometown = ndb.StringProperty()
    experience_work = ndb.StringProperty()
    experience_tagged_place = ndb.StringProperty()
    interest_music = ndb.StringProperty()
    interest_book = ndb.StringProperty()
    installed_apps = ndb.StringProperty()
    apps_category = ndb.StringProperty()
    vibrate_status = ndb.BooleanProperty()
    matched_with = ndb.IntegerProperty(default=None)
    willing = ndb.IntegerProperty(default=None)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

    def cal_sim_exp(self, other):
        """
        :type other: UserModel
        :rtype res:int
        """
        res = 0
        for i in self.experience_education.split(","):
            if i in other.experience_education:
                res += 3
        if self.experience_hometown == other.experience_hometown:
            res += 3
        for i in self.experience_work.split(","):
            if i in other.experience_work:
                res += 2
        for i in self.experience_tagged_place.split(","):
            if i in other.experience_tagged_place:
                res += 2
        return min(res, 10)

    def cal_sim_interest(self, other):
        """
        :type other: UserModel
        :rtype res:int
        """
        res = 0
        for i in self.interest_music.split(","):
            if i in other.interest_music:
                res += 3
        for i in self.interest_book.split(","):
            if i in other.interest_book:
                res += 3
        return min(res, 10)

    def cal_sim_apps(self, other):
        """
        :type other: UserModel
        :rtype res:int
        """
        res = 0
        for i in json.loads(self.installed_apps):
            if i in json.loads(other.installed_apps):
                res += 1
        my_app_cat = json.loads(self.apps_category)
        others_app_cat = json.loads(other.apps_category)
        res += int(5 * self._get_sim_vectors(my_app_cat.values(), others_app_cat.values()))
        return min(res, 10)

    def _get_sim_vectors(self, v1, v2):
        import numpy as np
        return 1 - np.linalg.norm(np.array(v1) - np.array(v2))
