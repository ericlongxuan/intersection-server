# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template

from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from forms import UserForm
from models import UserModel

from decorators import login_required


class AdminListUsers(View):

    @login_required
    def dispatch_request(self):
        users = UserModel.query()
        user_create_form = UserForm()

        if user_create_form.is_submitted():
            user = UserModel(
                name=user_create_form.name.data,
                gender="",
                uuid="",
                bluetooth="",
                facebook_id="",
                photo_url="",
                facebook_token="",
                gps="",
                experience_education="",
                experience_hometown="",
                experience_work="",
                experience_tagged_place="",
                interest_music="",
                interest_book="",
                installed_apps="",
                vibrate_status=False,
                matched_with=None
            )
            try:
                user.put()
                user_id = user.key.id()
                return redirect(url_for('admin_list_users'))
            except CapabilityDisabledError:
                flash(u'App Engine Datastore is currently in read-only mode.', 'info')
                return redirect(url_for('admin_list_users'))
        return render_template('list_users.html', users=users, form=user_create_form)