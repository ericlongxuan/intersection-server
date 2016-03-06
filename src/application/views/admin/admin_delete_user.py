# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, request

from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from models import UserModel

from decorators import login_required


class AdminDeleteUser(View):

    @login_required
    def dispatch_request(self, user_id):
        user = UserModel.get_by_id(int(user_id))
        if request.method == "POST":
            try:
                user.key.delete()
                flash(u'User %s successfully deleted.' % user_id, 'success')
                return redirect(url_for('admin_list_users'))
            except CapabilityDisabledError:
                flash(u'App Engine Datastore is currently in read-only mode.', 'info')
                return redirect(url_for('admin_list_users'))
