from django.urls import path
from . import views


urlpatterns = [
    # Página "Comece por aqui"
    path(
        '',
        views.home,
        name='home'
    ),

    # Página principal de notícias
    path(
        'noticias/',
        views.pagina_noticias,
        name='noticias'
    ),

    # Página individual de uma notícia
    path(
        'noticias/<slug:slug>/',
        views.noticia_detalhe,
        name='noticia_detalhe'
    ),
]