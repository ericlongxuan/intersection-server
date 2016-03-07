"""
models.py

App Engine datastore models

"""
import json, random

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
    features = ndb.StringProperty()  #[0,1,4]
    weights = ndb.StringProperty() #[0.33,0.33,0,0,0.33,0,0]
    gps = ndb.StringProperty()
    where = ndb.StringProperty()
    locations = ndb.StringProperty(default="")
    experience_education = ndb.StringProperty()
    experience_hometown = ndb.StringProperty()
    experience_work = ndb.StringProperty()
    experience_tagged_place = ndb.StringProperty()
    interest_music = ndb.StringProperty()
    interest_book = ndb.StringProperty()
    installed_apps = ndb.StringProperty(default="[]")
    apps_category = ndb.StringProperty(default=json.dumps({"Tools":0, "Music & Audio":0, "Finance":0, "Communication":0}))
    vibrate_status = ndb.BooleanProperty(default=0)
    matched_with = ndb.IntegerProperty(default=None)
    willing = ndb.IntegerProperty(default=5)
    speech_percent = ndb.FloatProperty(default=0.05)
    grades = ndb.StringProperty(default="{}") #recent 20 [{sim:[1,4,5,6,0,2,4], grade:2}]
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

    #"Experience", "Hobby", "InstalledApps", "Locations", "Sociability", "Sports", "Lifestyle"
    def cal_sim(self, other):
        """
        :type other: UserModel
        :rtype res:int
        """
        return [self.cal_sim_exp(other), self.cal_sim_interest(other),
                self.cal_sim_apps(other), self.cal_sim_loactions(other),
                self.cal_sim_social(other), self.cal_sim_sports(other),
                self.cal_sim_life(other)]

    def cal_grade(self, other):
        grade = 0
        weights = json.loads(self.weights)
        sim = self.cal_sim(other)
        for i in range(len(weights)):
            grade += weights[i] * sim[i]
        return min(max(0, int(round(grade))), 10)

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
        if not self.installed_apps or not other.installed_apps:
            return 0
        res = 0
        for i in json.loads(self.installed_apps):
            if i in json.loads(other.installed_apps):
                res += 1
        my_app_cat = json.loads(self.apps_category)
        others_app_cat = json.loads(other.apps_category)
        res += int(round(5.0 * self._get_sim_vectors(my_app_cat.values(), others_app_cat.values())))
        return min(res, 10)

    def cal_sim_loactions(self, other):
        """
        :type other: UserModel
        :rtype res:int
        """
        if not self.locations or not other.locations:
            return 0
        my_locs = [0]*10
        other_locs = [0]*10
        for i in self.locations:
            my_locs[int(i)] += 1
        for i in other.locations:
            other_locs[int(i)] += 1
        my_sum = sum(my_locs)
        other_sum = sum(other_locs)
        for idx in xrange(len(my_locs)):
            my_locs[idx] = float(my_locs[idx]) / my_sum
        for idx in xrange(len(other_locs)):
            other_locs[idx] = float(other_locs[idx]) / other_sum
        res = int(round((10.0 * self._get_sim_vectors(my_locs, other_locs))))
        return res

    def cal_sim_social(self, other):
        """
        :type other: UserModel
        :rtype res:int
        """
        if self.speech_percent == 0 and other.speech_percent == 0:
            return 10

        if self.speech_percent < other.speech_percent:
            a = self.speech_percent
            b = other.speech_percent
        else:
            b = self.speech_percent
            a = other.speech_percent
        return int(round(a / b * 10))

    def cal_sim_sports(self, other):
        """
        :type other: UserModel
        :rtype res:int
        """
        return random.randrange(0,11)

    def cal_sim_life(self, other):
        """
        :type other: UserModel
        :rtype res:int
        """
        return random.randrange(0,11)

    def _get_sim_vectors(self, v1, v2):
        import numpy as np
        return min(max(1 - np.linalg.norm(np.array(v1) - np.array(v2)),0),1)

