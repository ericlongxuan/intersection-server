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
        result["grades"] = []
        user = UserModel.get_by_id(int(user_id))
        if user.vibrate_status and user.matched_with is not None:
            user.vibrate_status = False
            user.put()
            match = UserModel.get_by_id(int(user.matched_with))
            result["is_matched"] = True
            result["user_id"] = match.key.id()
            result["name"] = match.name
            result["gender"] = match.gender
            result["photo_url"] = match.photo_url
            result["similarities"] = user.cal_sim(match)

        elif user.vibrate_status and user.matched_with is None:
            my_key = ndb.Key("UserModel", int(user_id))
            choose_keys = UserModel.query().fetch(keys_only=True)
            if my_key in choose_keys:
                choose_keys.remove(my_key)
                for choose_key in choose_keys:
                    match = choose_key.get()
                    if match.vibrate_status and match.matched_with is None and user.where is not None and match.where == user.where and user.cal_grade(match) > 10 - user.willing:
                        user.matched_with = match.key.id()
                        user.vibrate_status = False
                        user.put()
                        match.matched_with = int(user_id)
                        match.put()
                        result["is_matched"] = True
                        result["user_id"] = match.key.id()
                        result["name"] = match.name
                        result["gender"] = match.gender
                        result["photo_url"] = match.photo_url
                        result["similarities"] = user.cal_sim(match)
        return json.dumps(result)
