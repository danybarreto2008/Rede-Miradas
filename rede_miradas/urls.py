from django.urls import path

from . import views


# URLs do app rede_miradas
urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

]