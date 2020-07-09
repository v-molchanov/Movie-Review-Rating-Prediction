from django.contrib import admin
from django.urls import path

from movie_reviews_site.movie_reviews import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
]
