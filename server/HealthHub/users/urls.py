from django.urls import path

from . import views

urlpatterns = [
	path("create", views.createuser, name="createuser"),
	#path("settings/get", views.getsettings, name="getsettings"),
	#path("settings/edit", views.editsettings, name="editsettings"),
]