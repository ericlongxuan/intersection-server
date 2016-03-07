# -*- coding: utf-8 -*-

from flask import flash, redirect, url_for, render_template, request
from flask.views import View
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from models import UserModel
import json


class UserSetWilling(View):
    def dispatch_request(self, user_id, willing):
        user = UserModel.get_by_id(int(user_id))
        user.willing = int(willing)
        user.put()
        u_dict = user.to_dict()
        u_dict["user_id"] = user.key.id()
        del u_dict["timestamp"]
        return json.dumps(u_dict)

