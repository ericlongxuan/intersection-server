# -*- coding: utf-8 -*-
import json
import random

from google.appengine.ext import ndb

from flask import flash, redirect, url_for, render_template, request
from flask.views import View
from models import UserModel


class UserHasMatched(View):
    def dispatch_request(self, user_id):
        result = {}
        result["is_matched"] = False
        user = UserModel.get_by_id(int(user_id))
        if user.vibrate_status and user.matched_with is None:
            result["is_matched"] = True
            my_key = ndb.Key("UserModel", int(user_id))
            choose_keys = UserModel.query().fetch(keys_only=True)
            if my_key in choose_keys:
                choose_keys.remove(my_key)
                for choose_key in choose_keys:
                    match = choose_key.get()
                    if match.vibrate_status:
                        user.matched_with = match.key.id()
                        user.put()
                        match.matched_with = int(user_id)
                        match.put()
                        result["user_id"] = match.key.id()
                        result["name"] = match.name
                        result["gender"] = match.gender
                        result["photo_url"] = match.photo_url
                        result["similarities"] = [random.randrange(1,10) for i in range(7)]

        return json.dumps(result)
