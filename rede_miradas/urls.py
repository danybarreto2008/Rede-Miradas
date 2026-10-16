from django.urls import include, path

from . import admin_views, views

urlpatterns = [
    #Comece por aqui
    path("", views.home, name="home"),
    #Página principal de notícias
    path("noticias/", views.pagina_noticias, name="noticias"),
    path(
        "noticias/carregar-mais/",
        views.carregar_mais_noticias,
        name="carregar_mais_noticias",
    ),
    #Página inicial das Trilhas de Aprendizagem
    path("trilhas/", views.inicial_trilhas, name="inicial_trilhas"),
    #Página de visão geral das trilhas
    path(
        "trilhas/visao-geral/",
        views.trilhas_visao_geral,
        name="trilhas_visao_geral",
    ),
    #Página da 1ª trilha
    path(
        "trilhas/inscricao-das-equipes/",
        views.trilha_inscricao_equipes,
        name="trilha_inscricao_equipes",
    ),
    path(
        "trilhas/limpar-historico/",
        views.limpar_historico_trilhas,
        name="limpar_historico_trilhas",
    ),
    path(
        "trilhas/salvar-progresso/",
        views.salvar_progresso_trilha,
        name="salvar_progresso_trilha",
    ),
    #detalhe de uma trilha 
    path("trilhas/<slug:slug>/", views.trilha_detalhe, name="trilha_detalhe"),
    #Como tudo começou
    path(
        "como-tudo-comecou/", views.como_tudo_comecou, name="como_tudo_comecou"
    ),
    #detalhe de uma notícia
    path(
        "noticias/<slug:slug>/", views.noticia_detalhe, name="noticia_detalhe"
    ),
    # login
    path("accounts/", include("allauth.urls")),
    path("pos-login/", views.redirecionar_apos_login, name="pos_login"),
    path("login-superadmin/", views.login_superadmin, name="login_superadmin"),
    path("painel/aluno/", views.painel_aluno, name="painel_aluno"),
    path("painel/professor/", views.painel_professor, name="painel_professor"),
    path("votacao/", views.votacao, name="votacao"),
    path("perfil/", views.meu_perfil, name="meu_perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),
    path(
        "selos/confirmar/<int:conquista_id>/",
        views.confirmar_selo,
        name="confirmar_selo",
    ),
    #painel administrativo
    path("painel/admin/", admin_views.admin_dashboard, name="painel_admin"),
    path(
        "painel/admin/logout/", admin_views.logout_admin, name="logout_admin"
    ),
    path(
        "painel/admin/destaques/",
        admin_views.admin_destaques_lista,
        name="admin_destaques_lista",
    ),
    path(
        "painel/admin/destaques/novo/",
        admin_views.admin_destaque_novo,
        name="admin_destaque_novo",
    ),
    path(
        "painel/admin/destaques/<int:id>/editar/",
        admin_views.admin_destaque_editar,
        name="admin_destaque_editar",
    ),
    path(
        "painel/admin/destaques/<int:id>/excluir/",
        admin_views.admin_destaque_excluir,
        name="admin_destaque_excluir",
    ),
    path(
        "painel/admin/destaques/<int:id>/toggle/",
        admin_views.admin_destaque_toggle,
        name="admin_destaque_toggle",
    ),
    path(
        "painel/admin/blocos/",
        admin_views.admin_blocos_lista,
        name="admin_blocos_lista",
    ),
    path(
        "painel/admin/blocos/novo/",
        admin_views.admin_bloco_novo,
        name="admin_bloco_novo",
    ),
    path(
        "painel/admin/blocos/<int:id>/editar/",
        admin_views.admin_bloco_editar,
        name="admin_bloco_editar",
    ),
    path(
        "painel/admin/blocos/<int:id>/excluir/",
        admin_views.admin_bloco_excluir,
        name="admin_bloco_excluir",
    ),
    path(
        "painel/admin/blocos/<int:id>/toggle/",
        admin_views.admin_bloco_toggle,
        name="admin_bloco_toggle",
    ),
    path(
        "painel/admin/curtas-home/",
        admin_views.admin_curtas_home_lista,
        name="admin_curtas_home_lista",
    ),
    path(
        "painel/admin/curtas-home/novo/",
        admin_views.admin_curta_home_novo,
        name="admin_curta_home_novo",
    ),
    path(
        "painel/admin/curtas-home/<int:id>/editar/",
        admin_views.admin_curta_home_editar,
        name="admin_curta_home_editar",
    ),
    path(
        "painel/admin/curtas-home/<int:id>/excluir/",
        admin_views.admin_curta_home_excluir,
        name="admin_curta_home_excluir",
    ),
    path(
        "painel/admin/curtas-home/<int:id>/toggle/",
        admin_views.admin_curta_home_toggle,
        name="admin_curta_home_toggle",
    ),
    path(
        "painel/admin/secoes-home/",
        admin_views.admin_secoes_home,
        name="admin_secoes_home",
    ),
    # Notícias
    path(
        "painel/admin/noticias/",
        admin_views.admin_noticias_lista,
        name="admin_noticias_lista",
    ),
    path(
        "painel/admin/noticias/nova/",
        admin_views.admin_noticia_nova,
        name="admin_noticia_nova",
    ),
    path(
        "painel/admin/noticias/<int:id>/editar/",
        admin_views.admin_noticia_editar,
        name="admin_noticia_editar",
    ),
    path(
        "painel/admin/noticias/<int:id>/excluir/",
        admin_views.admin_noticia_excluir,
        name="admin_noticia_excluir",
    ),
    path(
        "painel/admin/noticias/<int:id>/toggle-pub/",
        admin_views.admin_noticia_toggle_pub,
        name="admin_noticia_toggle_pub",
    ),
    path(
        "painel/admin/noticias/<int:id>/toggle-destaque/",
        admin_views.admin_noticia_toggle_destaque,
        name="admin_noticia_toggle_destaque",
    ),
    # Trilhas de Aprendizagem
    path(
        "painel/admin/trilhas/",
        admin_views.admin_trilhas_dashboard,
        name="admin_trilhas_dashboard",
    ),
    path(
        "painel/admin/trilhas/hero/",
        admin_views.admin_trilhas_hero,
        name="admin_trilhas_hero",
    ),
    path(
        "painel/admin/trilhas/faixa/",
        admin_views.admin_trilhas_faixa_lista,
        name="admin_trilhas_faixa_lista",
    ),
    path(
        "painel/admin/trilhas/faixa/novo/",
        admin_views.admin_trilhas_faixa_novo,
        name="admin_trilhas_faixa_novo",
    ),
    path(
        "painel/admin/trilhas/faixa/<int:id>/editar/",
        admin_views.admin_trilhas_faixa_editar,
        name="admin_trilhas_faixa_editar",
    ),
    path(
        "painel/admin/trilhas/faixa/<int:id>/excluir/",
        admin_views.admin_trilhas_faixa_excluir,
        name="admin_trilhas_faixa_excluir",
    ),
    path(
        "painel/admin/trilhas/faixa/<int:id>/toggle/",
        admin_views.admin_trilhas_faixa_toggle,
        name="admin_trilhas_faixa_toggle",
    ),
    #Cards
    path(
        "painel/admin/trilhas/cards/",
        admin_views.admin_trilhas_cards_lista,
        name="admin_trilhas_cards_lista",
    ),
    path(
        "painel/admin/trilhas/cards/novo/",
        admin_views.admin_trilha_card_novo,
        name="admin_trilha_card_novo",
    ),
    path(
        "painel/admin/trilhas/cards/<int:id>/editar/",
        admin_views.admin_trilha_card_editar,
        name="admin_trilha_card_editar",
    ),
    path(
        "painel/admin/trilhas/cards/<int:id>/excluir/",
        admin_views.admin_trilha_card_excluir,
        name="admin_trilha_card_excluir",
    ),
    path(
        "painel/admin/trilhas/cards/<int:id>/toggle/",
        admin_views.admin_trilha_card_toggle,
        name="admin_trilha_card_toggle",
    ),
    #Unidades
    path(
        "painel/admin/trilhas/unidades/",
        admin_views.admin_unidades_lista,
        name="admin_unidades_lista",
    ),
    path(
        "painel/admin/trilhas/unidades/nova/",
        admin_views.admin_unidade_nova,
        name="admin_unidade_nova",
    ),
    path(
        "painel/admin/trilhas/unidades/<int:id>/editar/",
        admin_views.admin_unidade_editar,
        name="admin_unidade_editar",
    ),
    path(
        "painel/admin/trilhas/unidades/<int:id>/excluir/",
        admin_views.admin_unidade_excluir,
        name="admin_unidade_excluir",
    ),
    #Tópicos
    path(
        "painel/admin/trilhas/topicos/",
        admin_views.admin_topicos_lista,
        name="admin_topicos_lista",
    ),
    path(
        "painel/admin/trilhas/topicos/novo/",
        admin_views.admin_topico_novo,
        name="admin_topico_novo",
    ),
    path(
        "painel/admin/trilhas/topicos/<int:id>/editar/",
        admin_views.admin_topico_editar,
        name="admin_topico_editar",
    ),
    path(
        "painel/admin/trilhas/topicos/<int:id>/excluir/",
        admin_views.admin_topico_excluir,
        name="admin_topico_excluir",
    ),
    #Subtópicos Rápidos
    path(
        "painel/admin/trilhas/subtopicos/",
        admin_views.admin_subtopicos_lista,
        name="admin_subtopicos_lista",
    ),
    path(
        "painel/admin/trilhas/subtopicos/novo/",
        admin_views.admin_subtopico_novo,
        name="admin_subtopico_novo",
    ),
    path(
        "painel/admin/trilhas/subtopicos/<int:id>/editar/",
        admin_views.admin_subtopico_editar,
        name="admin_subtopico_editar",
    ),
    path(
        "painel/admin/trilhas/subtopicos/<int:id>/excluir/",
        admin_views.admin_subtopico_excluir,
        name="admin_subtopico_excluir",
    ),
    # Votação do Júri Popular
    path(
        "painel/admin/votacao/",
        admin_views.admin_votacao,
        name="admin_votacao",
    ),
    path(
        "painel/admin/votacao/novo/",
        admin_views.admin_curta_votacao_novo,
        name="admin_curta_votacao_novo",
    ),
    path(
        "painel/admin/votacao/<int:id>/editar/",
        admin_views.admin_curta_votacao_editar,
        name="admin_curta_votacao_editar",
    ),
    path(
        "painel/admin/votacao/<int:id>/excluir/",
        admin_views.admin_curta_votacao_excluir,
        name="admin_curta_votacao_excluir",
    ),
    path(
        "painel/admin/votacao/<int:id>/toggle/",
        admin_views.admin_curta_votacao_toggle,
        name="admin_curta_votacao_toggle",
    ),
    path(
        "painel/admin/usuarios/",
        admin_views.admin_usuarios_lista,
        name="admin_usuarios_lista",
    ),
    path(
        "painel/admin/usuarios/<int:user_id>/perfil/",
        admin_views.admin_perfil_editar,
        name="admin_perfil_editar",
    ),
    path(
        "painel/admin/usuarios/<int:user_id>/excluir/",
        admin_views.admin_usuario_excluir,
        name="admin_usuario_excluir",
    ),
]
