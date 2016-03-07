# -*- coding: utf-8 -*-
import googlemaps, json

from flask.views import View
from models import UserModel


class UserUpdateAudio(View):

    def dispatch_request(self, user_id, speech_percent):
        user = UserModel.get_by_id(int(user_id))
        user.speech_percent = float(speech_percent)
        user.put()
        u_dict = user.to_dict()
        u_dict["user_id"] = user.key.id()
        del u_dict["timestamp"]
        return json.dumps(u_dict)