# -*- coding: utf-8 -*-

from flask import flash, redirect, url_for, render_template, request
from flask.views import View
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from models import UserModel
import json, math, random


class UserGradeOther(View):
    def dispatch_request(self, user_id, other_id, grading):
        if grading == "0":
            grading = str(random.randrange(0,5))
        else:
            grading = str(random.randrange(5,10))
        user = UserModel.get_by_id(int(user_id))
        other = UserModel.get_by_id(int(other_id))
        sim = user.cal_sim(other)
        features = json.loads(user.features)
        grade_his = json.loads(user.grades)
        sim_in_feature = [sim[i] for i in features]
        sim_str = str(sim_in_feature)
        if sim_str in grade_his:
            grade_his[sim_str] = grading
        else:
            if len(grade_his) > 15:
                del(grade_his[grade_his.keys()[0]])
            grade_his[sim_str] =  grading
        user.grades = json.dumps(grade_his)

        if len(grade_his) >= 3:
            import numpy as np
            x = []
            y = []
            for key, value in grade_his.items():
                x.append(json.loads(key))
                y.append(int(value))
            xMat = np.mat(x)
            yMat = np.mat(y).T
            xTx = xMat.T * xMat
            if np.linalg.det(xTx) == 0.0:
                #user.put()
                return "canot do inverse" + json.dumps(user.grades)

            weights_learnt_matrix = xTx.I*(xMat.T*yMat)
            weights_learnt = [a[0] for a in weights_learnt_matrix.tolist()]
            weights = [0] * 7
            for i in range(len(weights_learnt)):
                weights[features[i]] = weights_learnt[i]
            user.weights = json.dumps(weights)

        user.put()
        u_dict = user.to_dict()
        u_dict["user_id"] = user.key.id()
        del u_dict["timestamp"]
        return json.dumps(u_dict)