"""
urls.py

URL dispatch route mappings and error handlers

"""
from application import app
from application.views.admin.admin_list_users import AdminListUsers
from application.views.public.public_index import PublicIndex
from application.views.public.public_say_hello import PublicSayHello
from application.views.public.public_warmup import PublicWarmup
from flask import render_template
# from application.views.admin.admin_list_examples_cached import AdminListExamplesCached
from application.views.admin.admin_secret import AdminSecret
from application.views.admin.admin_delete_user import AdminDeleteUser
from application.views.admin.admin_set_vibrate import AdminSetVibrate

from application.views.user.user_create import UserCreate
from application.views.user.user_has_matched import UserHasMatched
from application.views.user.user_upload_gps import UserUploadGps
from application.views.user.user_set_features import UserSetFeatures
from application.views.user.user_others_to_grade import UseOthersToGrade


# URL dispatch rules

# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

app.add_url_rule('/_ah/warmup', 'public_warmup', view_func=PublicWarmup.as_view('public_warmup'))

app.add_url_rule('/', 'public_index', view_func=PublicIndex.as_view('public_index'))

app.add_url_rule('/hello/<username>/<gps>', 'public_say_hello', view_func=PublicSayHello.as_view('public_say_hello'))

app.add_url_rule('/register', 'user_create', view_func=UserCreate.as_view('user_create'), methods=['GET', 'POST'])
app.add_url_rule('/is_matched/<user_id>', 'user_has_matched', view_func=UserHasMatched.as_view('user_has_matched'))
app.add_url_rule('/others_to_grade/<user_id>/<count>', 'user_others_to_grade', view_func=UseOthersToGrade.as_view('user_others_to_grade'))
app.add_url_rule('/upload_gps/<user_id>/<gps>', 'user_upload_gps', view_func=UserUploadGps.as_view('user_upload_gps'), methods=['GET', 'POST'])
app.add_url_rule('/set_features/<user_id>/<features>', 'user_set_features', view_func=UserSetFeatures.as_view('user_set_features'))

app.add_url_rule('/admin/users', 'admin_list_users', view_func=AdminListUsers.as_view('admin_list_users'), methods=['GET', 'POST'])
app.add_url_rule('/admin/delete_user/<user_id>', 'admin_delete_user', view_func=AdminDeleteUser.as_view('admin_delete_user'), methods=['POST'])
app.add_url_rule('/admin/set_vibrate/<user_id>/<vib>', 'admin_set_vibrate1', view_func=AdminSetVibrate.as_view('admin_set_vibrate1'))
app.add_url_rule('/admin/set_vibrate/<user_id>/<vib>/<matched_with>', 'admin_set_vibrate', view_func=AdminSetVibrate.as_view('admin_set_vibrate'))


# app.add_url_rule('/examples/cached', 'cached_examples', view_func=AdminListExamplesCached.as_view('cached_examples'))

app.add_url_rule('/admin_only', 'admin_only', view_func=AdminSecret.as_view('admin_only'))

# Error handlers

# Handle 404 errors


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
