# -*- coding: utf-8 -*-

import json
from flask.views import View
from flask import request
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from models import UserModel


class UserCreate(View):
    def dispatch_request(self):
        res = {}
        info = request.json
        try:
            #facebook_id = info["FacebookID"]
            # existed_user = UserModel.query().filter("facebook_id = ", facebook_id)
            # if existed_user:
            #     res["status"] = "fail"
            #     res["error"] = "UserExisted"
            #     return json.dumps(res)

            fb_info = info["FBinfo"]
            tagged_places = [p["place"]["location"]["city"] for p in fb_info["tagged_places"]["data"]] if fb_info["tagged_places"] else []
            tagged_places = list(set(tagged_places))
            installed_app = []
            apps_category = {"Tools":0, "Music & Audio":0, "Finance":0, "Communication":0}
            for app in info["app"]["apps"]:
                if app["category"] in apps_category:
                    installed_app.append(app["title"])
                    apps_category[app["category"]] += 1
            user = UserModel(
                name=fb_info["name"],
                gender=fb_info["gender"],
                uuid="",
                bluetooth="",
                facebook_id=info["FacebookID"],
                photo_url=info["photo URL"],
                facebook_token=info["AccessToken"],
                gps="",
                experience_education=",".join([s["school"]["name"] for s in fb_info["education"]]),
                experience_hometown="" if "name" not in fb_info["hometown"] else fb_info["hometown"]["name"],
                experience_work=",".join([w["employer"]["name"] for w in fb_info["work"]]),
                experience_tagged_place=",".join(tagged_places),
                interest_music=",".join([m["name"] for m in fb_info["music"]["data"]]),
                interest_book=",".join([b["name"] for b in fb_info["books"]["data"]]),
                #installed_apps=json.dumps(apps),
                installed_apps=json.dumps(installed_app),
                apps_category=json.dumps(apps_category),
                vibrate_status=False,
                matched_with=None
            )
            user.put()
            user_id = user.key.id()
            res["user_id"] = user_id
            res["status"] = "succeed"
            return json.dumps(res)
        except Exception as e:
            res["status"] = "fail"
            res["error"] = e.message
            return json.dumps(res)
        # try:
        #     user.put()
        #     user_id = user.key.id()
        #     res["user_id"] = user_id
        #     res["status"] = "succeed"
        #     return json.dumps(res)
        # except CapabilityDisabledError:
        #     res["status"] = "fail"
        #     res["error"] = "CapacityDisable"
        #     return json.dumps(res)

