from django.urls import path

from . import views

urlpatterns = [
	#path("exerciseplan", views.exerciseplan, name="exerciseplan"),
	#path("mealplan", views.mealplan, name="mealplan"),
	#path("sleepplan", views.sleepplan, name="sleepplan"),
	path("chooseplan", views.chooseplan, name="chooseplan"),
]