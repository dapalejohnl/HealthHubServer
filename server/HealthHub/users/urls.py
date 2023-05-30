from django.urls import path

from . import views

urlpatterns = [
	path("create", views.createuser, name="createuser"),
	path("login", views.login, name="login"),
	path("logout", views.logout, name="logout"),
	#path("settings/get", views.getsettings, name="getsettings"),
	#path("settings/edit", views.editsettings, name="editsettings"),
]