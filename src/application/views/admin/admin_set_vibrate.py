# -*- coding: utf-8 -*-

from flask import flash, redirect, url_for, render_template, request
from flask.views import View
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from models import UserModel
import json


class AdminSetVibrate(View):

    def dispatch_request(self, user_id, vib, matched_with=None):
        user = UserModel.get_by_id(int(user_id))
        user.vibrate_status = bool(int(vib))
        if not user.vibrate_status:
            user.matched_with = None
        if matched_with:
            user.matched_with = int(matched_with)
        user.put()
        u_dict = user.to_dict()
        u_dict["user_id"] = user.key.id()
        del u_dict["timestamp"]
        return json.dumps(u_dict)

