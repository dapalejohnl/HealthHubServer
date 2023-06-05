from django.urls import path

from . import views

urlpatterns = [
	path("get", views.getplans, name="getplans"),
	path("chooseplan", views.chooseplan, name="chooseplan"),
]