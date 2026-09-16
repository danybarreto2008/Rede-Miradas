from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import LoginRedirecionadoView


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
    #login
    path('cadastro/aluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('cadastro/professor/', views.cadastro_professor, name='cadastro_professor'),

    path('login/', LoginRedirecionadoView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('login-superadmin/', views.login_superadmin, name='login_superadmin'),

    path('painel/aluno/', views.painel_aluno, name='painel_aluno'),
    path('painel/professor/', views.painel_professor, name='painel_professor'),
]