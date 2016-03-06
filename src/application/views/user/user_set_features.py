# -*- coding: utf-8 -*-

from flask import flash, redirect, url_for, render_template, request
from flask.views import View
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from models import UserModel
import json


class UserSetFeatures(View):
    def dispatch_request(self, user_id, features):
        user = UserModel.get_by_id(int(user_id))
        user.features = "[" + features + "]"
        weights = [0] * 7
        features_list = features.split(",")
        for f in features_list:
            weights[int(f)] = 1.0/ len(features_list)
        user.weights = str(weights)
        user.put()
        u_dict = user.to_dict()
        u_dict["user_id"] = user.key.id()
        del u_dict["timestamp"]
        return json.dumps(u_dict)

