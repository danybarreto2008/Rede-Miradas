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

    # Carregar mais posts (precisa vir ANTES da rota de slug,
    # senão "carregar-mais" é interpretado como um slug de notícia)
    path(
        'noticias/carregar-mais/',
        views.carregar_mais_noticias,
        name='carregar_mais_noticias'
    ),

    # Página inicial das Trilhas de Aprendizagem
    path(
        'trilhas/',
        views.inicial_trilhas,
        name='inicial_trilhas'
    ),

    # Página de visão geral das trilhas
    path(
        'trilhas/visao-geral/',
        views.trilhas_visao_geral,
        name='trilhas_visao_geral'
    ),

    # Página individual de uma notícia
    # (sempre por último, pois <slug:slug> combina com qualquer texto)
    path(
        'noticias/<slug:slug>/',
        views.noticia_detalhe,
        name='noticia_detalhe'
    ),
]