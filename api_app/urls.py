from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /user/signup
    url(r'^signup', views.signup_view, name = "signup_view"),
	# ex: /user/login
    url(r'^login', views.login_view, name = "login_view"),
	# ex: /user/logout
    url(r'^logout', views.logout_view, name = "logout_view"),
    # ex: /user/sahil
    url(r'^(?P<username>[^/]+)/?$', views.user_data_view, name = "user_data_view"),
]