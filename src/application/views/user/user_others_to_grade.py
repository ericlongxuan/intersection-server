# -*- coding: utf-8 -*-
import random

from google.appengine.ext import ndb

from flask import flash, redirect, url_for, render_template, request
from flask.views import View
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from models import UserModel
import json


class UseOthersToGrade(View):
    def dispatch_request(self, user_id, count):
        my_key = ndb.Key("UserModel", int(user_id))
        others = []
        if UserModel.query().count() <= 1:
            return json.dumps(others)

        choose_keys = UserModel.query().fetch(keys_only=True)
        if my_key in choose_keys:
            choose_keys.remove(my_key)
        if len(choose_keys) > count:
            choose_keys = random.sample(choose_keys, count)

        dataset = [k.get() for k in choose_keys]
        for other in dataset:
            other_dic = {}
            other_dic["user_id"] = other.key.id()
            other_dic["photo_url"] = other.photo_url
            other_dic["similarities"] = [random.randrange(1,10) for i in range(7)]
            others.append(other_dic)
        return json.dumps(others)

