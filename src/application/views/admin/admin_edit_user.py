# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template, request

from forms import UserForm
from models import UserModel

from decorators import login_required


class AdminEditUser(View):

    @login_required
    def dispatch_request(self, user_id):
        user = UserModel.get_by_id(user_id)
        form = UserForm(obj=user)
        if request.method == "POST":
            if form.validate_on_submit():
                user.name = form.data.get('name')
                user.put()
                flash(u'Example %s successfully saved.' % user_id, 'success')
                return redirect(url_for('list_examples'))
        return render_template('edit_user.html', user=user, form=form)
