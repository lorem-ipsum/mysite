from django.urls import path

from . import views

urlpatterns = [
    path('movies/', views.movies),
    path('movies/<int:mid>/', views.movie),
    path('characters/', views.characters),
    path('characters/<int:cid>/', views.character),
    path('comments/<int:cmid>/', views.comment),
    path('search/', views.search),
]
