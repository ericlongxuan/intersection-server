# -*- coding: utf-8 -*-

from flask.views import View

from flask import redirect, url_for


class PublicIndex(View):

    def dispatch_request(self):
        return redirect(url_for('admin_list_users'))
