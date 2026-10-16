from functools import reduce, wraps
from operator import or_

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
)
from django.contrib.auth import (
    login as auth_login,
)
from django.contrib.auth import (
    logout as auth_logout,
)
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .admin_forms import (
    BlocoApresentacaoForm,
    CurtaForm,
    CurtaVotacaoForm,
    DestaqueForm,
    NoticiaForm,
    PerfilAdminForm,
    SecaoCurtasForm,
    SecaoFinalForm,
    SubtopicoTrilhaForm,
    TopicoUnidadeTrilhaForm,
    TrilhasCardForm,
    TrilhasFaixaItemForm,
    TrilhasHeroForm,
    UnidadeTrilhaForm,
)
from .models import (
    BlocoApresentacao,
    Curta,
    CurtaVotacao,
    Destaque,
    Noticia,
    Perfil,
    SecaoCurtas,
    SecaoFinal,
    SubtopicoTrilha,
    TopicoUnidadeTrilha,
    TrilhasCard,
    TrilhasFaixaItem,
    TrilhasHero,
    UnidadeTrilha,
    Voto,
)


def admin_required(view_func):
    """
    Decorator que garante que apenas superusuários ou membros da equipe (staff)
    tenham acesso às páginas administrativas.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                request,
                "Faça login com sua conta de administrador para "
                "acessar o painel.",
            )
            return redirect("login_superadmin")
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(
                request,
                "Acesso negado: esta área é restrita a "
                "administradores do sistema.",
            )
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


# autenticação do administrador


def login_superadmin(request):
    """
    Página de login dedicada e estilizada para o administrador.
    Redireciona diretamente para o novo Dashboard Administrativo.
    """
    if request.user.is_authenticated and (
        request.user.is_superuser or request.user.is_staff
    ):
        return redirect("painel_admin")

    erro = None
    if request.method == "POST":
        identificador = request.POST.get("username", "").strip()
        senha = request.POST.get("password", "")

        username_auth = identificador
        if "@" in identificador:
            user_com_email = User.objects.filter(
                email__iexact=identificador
            ).first()
            if user_com_email:
                username_auth = user_com_email.username

        usuario = authenticate(
            request, username=username_auth, password=senha
        )
        if usuario is not None and (usuario.is_superuser or usuario.is_staff):
            auth_login(request, usuario)
            nome_usuario = usuario.first_name or usuario.username
            messages.success(
                request,
                f"Bem-vindo(a) ao painel administrativo, {nome_usuario}!",
            )
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("painel_admin")
        else:
            erro = (
                "Credenciais inválidas ou o usuário não possui "
                "permissão de administrador."
            )

    return render(request, "rede_miradas/admin/login.html", {"erro": erro})


@admin_required
def logout_admin(request):
    auth_logout(request)
    messages.info(
        request, "Você encerrou sua sessão de administrador com segurança."
    )
    return redirect("login_superadmin")


# dashboard admin


@admin_required
def admin_dashboard(request):
    # Métricas
    total_noticias = Noticia.objects.count()
    noticias_publicadas = Noticia.objects.filter(publicada=True).count()
    noticias_destaque = Noticia.objects.filter(destaque=True).count()

    total_destaques = Destaque.objects.count()
    destaques_ativos = Destaque.objects.filter(ativo=True).count()

    total_blocos = BlocoApresentacao.objects.count()
    total_curtas_home = Curta.objects.count()

    total_trilhas = TrilhasCard.objects.count()
    trilhas_ativas = TrilhasCard.objects.filter(ativo=True).count()
    total_unidades = UnidadeTrilha.objects.count()
    total_topicos = TopicoUnidadeTrilha.objects.count()

    total_curtas_votacao = CurtaVotacao.objects.count()
    total_votos = Voto.objects.count()

    total_usuarios = User.objects.count()
    total_perfis = Perfil.objects.count()
    total_alunos = Perfil.objects.filter(tipo=Perfil.ALUNO).count()
    total_professores = Perfil.objects.filter(tipo=Perfil.PROFESSOR).count()

    # Itens recentes para a visão geral
    ultimas_noticias = Noticia.objects.order_by("-data_publicacao")[:5]
    destaques_recentes = Destaque.objects.order_by("ordem")[:4]
    curtas_top_votos = CurtaVotacao.objects.annotate(
        votos_count=Count("votos")
    ).order_by("-votos_count")[:4]

    context = {
        "total_noticias": total_noticias,
        "noticias_publicadas": noticias_publicadas,
        "noticias_destaque": noticias_destaque,
        "total_destaques": total_destaques,
        "destaques_ativos": destaques_ativos,
        "total_blocos": total_blocos,
        "total_curtas_home": total_curtas_home,
        "total_trilhas": total_trilhas,
        "trilhas_ativas": trilhas_ativas,
        "total_unidades": total_unidades,
        "total_topicos": total_topicos,
        "total_curtas_votacao": total_curtas_votacao,
        "total_votos": total_votos,
        "total_usuarios": total_usuarios,
        "total_perfis": total_perfis,
        "total_alunos": total_alunos,
        "total_professores": total_professores,
        "ultimas_noticias": ultimas_noticias,
        "destaques_recentes": destaques_recentes,
        "curtas_top_votos": curtas_top_votos,
    }
    return render(request, "rede_miradas/admin/dashboard.html", context)


# banners


@admin_required
def admin_destaques_lista(request):
    destaques = Destaque.objects.order_by("ordem", "id")
    return render(
        request,
        "rede_miradas/admin/destaques_lista.html",
        {"destaques": destaques},
    )


@admin_required
def admin_destaque_novo(request):
    if request.method == "POST":
        form = DestaqueForm(request.POST, request.FILES)
        if form.is_valid():
            destaque = form.save()
            titulo_dest = destaque.titulo or destaque.id
            messages.success(
                request,
                f'Destaque "{titulo_dest}" criado com sucesso!',
            )
            return redirect("admin_destaques_lista")
    else:
        form = DestaqueForm(
            initial={
                "ativo": True,
                "mostrar_botao": True,
                "ordem": Destaque.objects.count() + 1,
                "cor_titulo": "#FFFFFF",
                "cor_texto": "#FFFFFF",
                "cor_fundo_botao": "#FFFFFF",
                "cor_texto_botao": "#000000",
                "cor_borda_botao": "#FFFFFF",
                "posicao_horizontal": "esquerda",
                "posicao_vertical": "meio",
            }
        )
    return render(
        request,
        "rede_miradas/admin/destaque_form.html",
        {"form": form, "titulo_acao": "Novo Destaque da Tela Inicial"},
    )


@admin_required
def admin_destaque_editar(request, id):
    destaque = get_object_or_404(Destaque, id=id)
    if request.method == "POST":
        form = DestaqueForm(request.POST, request.FILES, instance=destaque)
        if form.is_valid():
            destaque = form.save()
            titulo_dest = destaque.titulo or destaque.id
            messages.success(
                request,
                f'Destaque "{titulo_dest}" atualizado com sucesso!',
            )
            return redirect("admin_destaques_lista")
    else:
        form = DestaqueForm(instance=destaque)
    return render(
        request,
        "rede_miradas/admin/destaque_form.html",
        {
            "form": form,
            "destaque": destaque,
            "titulo_acao": f"Editar Destaque #{destaque.id}",
        },
    )


@admin_required
def admin_destaque_excluir(request, id):
    destaque = get_object_or_404(Destaque, id=id)
    if request.method == "POST":
        titulo = destaque.titulo or f"Destaque #{destaque.id}"
        destaque.delete()
        messages.success(request, f'Destaque "{titulo}" excluído com sucesso.')
        return redirect("admin_destaques_lista")
    return render(
        request,
        "rede_miradas/admin/confirmar_exclusao.html",
        {
            "objeto": destaque,
            "tipo": "Destaque da Tela Inicial",
            "url_cancelar": "admin_destaques_lista",
        },
    )


@admin_required
def admin_destaque_toggle(request, id):
    if not (
        request.user.is_superuser
        or request.user.has_perm("rede_miradas.pode_gerenciar_destaques")
    ):
        messages.error(
            request, "Você não possui permissão para gerenciar destaques."
        )
        return redirect("admin_destaques_lista")
    destaque = get_object_or_404(Destaque, id=id)
    destaque.ativo = not destaque.ativo
    destaque.save()
    status = "ativado" if destaque.ativo else "desativado"
    messages.info(request, f"Destaque #{destaque.id} {status}.")
    return redirect("admin_destaques_lista")


# blocos de apresentação


@admin_required
def admin_blocos_lista(request):
    blocos = BlocoApresentacao.objects.order_by("ordem", "id")
    return render(
        request, "rede_miradas/admin/blocos_lista.html", {"blocos": blocos}
    )


@admin_required
def admin_bloco_novo(request):
    if request.method == "POST":
        form = BlocoApresentacaoForm(request.POST)
        if form.is_valid():
            bloco = form.save()
            resumo_bloco = bloco.texto[:25]
            messages.success(
                request,
                f'Bloco "{bloco.emoji} {resumo_bloco}" criado!',
            )
            return redirect("admin_blocos_lista")
    else:
        form = BlocoApresentacaoForm(
            initial={
                "ativo": True,
                "ordem": BlocoApresentacao.objects.count() + 1,
                "cor_gradiente_1": "#8b2ff7",
                "cor_gradiente_2": "#22d3ee",
            }
        )
    return render(
        request,
        "rede_miradas/admin/bloco_form.html",
        {"form": form, "titulo_acao": "Novo Bloco de Apresentação"},
    )


@admin_required
def admin_bloco_editar(request, id):
    bloco = get_object_or_404(BlocoApresentacao, id=id)
    if request.method == "POST":
        form = BlocoApresentacaoForm(request.POST, instance=bloco)
        if form.is_valid():
            form.save()
            messages.success(request, "Bloco de apresentação atualizado!")
            return redirect("admin_blocos_lista")
    else:
        form = BlocoApresentacaoForm(instance=bloco)
    return render(
        request,
        "rede_miradas/admin/bloco_form.html",
        {
            "form": form,
            "bloco": bloco,
            "titulo_acao": "Editar Bloco de Apresentação",
        },
    )


@admin_required
def admin_bloco_excluir(request, id):
    bloco = get_object_or_404(BlocoApresentacao, id=id)
    if request.method == "POST":
        bloco.delete()
        messages.success(
            request, "Bloco de apresentação excluído com sucesso."
        )
        return redirect("admin_blocos_lista")
    return render(
        request,
        "rede_miradas/admin/confirmar_exclusao.html",
        {
            "objeto": bloco,
            "tipo": "Bloco de Apresentação",
            "url_cancelar": "admin_blocos_lista",
        },
    )


@admin_required
def admin_bloco_toggle(request, id):
    bloco = get_object_or_404(BlocoApresentacao, id=id)
    bloco.ativo = not bloco.ativo
    bloco.save()
    status = "ativado" if bloco.ativo else "desativado"
    messages.info(request, f"Bloco {status}.")
    return redirect("admin_blocos_lista")


# curtas destaque


@admin_required
def admin_curtas_home_lista(request):
    curtas = Curta.objects.order_by("ordem", "id")
    return render(
        request,
        "rede_miradas/admin/curtas_home_lista.html",
        {"curtas": curtas},
    )


@admin_required
def admin_curta_home_novo(request):
    if request.method == "POST":
        form = CurtaForm(request.POST, request.FILES)
        if form.is_valid():
            curta = form.save()
            messages.success(
                request, f'Curta "{curta.nome}" cadastrado com sucesso!'
            )
            return redirect("admin_curtas_home_lista")
    else:
        form = CurtaForm(
            initial={
                "ativo": True,
                "ordem": Curta.objects.count() + 1,
                "cor_borda_1": "#7C3AED",
                "cor_borda_2": "#06B6D4",
            }
        )
    return render(
        request,
        "rede_miradas/admin/curta_home_form.html",
        {"form": form, "titulo_acao": "Novo Curta em Destaque"},
    )


@admin_required
def admin_curta_home_editar(request, id):
    curta = get_object_or_404(Curta, id=id)
    if request.method == "POST":
        form = CurtaForm(request.POST, request.FILES, instance=curta)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Curta "{curta.nome}" atualizado com sucesso!'
            )
            return redirect("admin_curtas_home_lista")
    else:
        form = CurtaForm(instance=curta)
    return render(
        request,
        "rede_miradas/admin/curta_home_form.html",
        {
            "form": form,
            "curta": curta,
            "titulo_acao": f"Editar Curta: {curta.nome}",
        },
    )


@admin_required
def admin_curta_home_excluir(request, id):
    curta = get_object_or_404(Curta, id=id)
    if request.method == "POST":
        curta.delete()
        messages.success(
            request, f'Curta "{curta.nome}" excluído com sucesso.'
        )
        return redirect("admin_curtas_home_lista")
    return render(
        request,
        "rede_miradas/admin/confirmar_exclusao.html",
        {
            "objeto": curta,
            "tipo": "Curta em Destaque na Tela Inicial",
            "url_cancelar": "admin_curtas_home_lista",
        },
    )


@admin_required
def admin_curta_home_toggle(request, id):
    curta = get_object_or_404(Curta, id=id)
    curta.ativo = not curta.ativo
    curta.save()
    status = "ativado" if curta.ativo else "desativado"
    messages.info(request, f'Curta "{curta.nome}" {status}.')
    return redirect("admin_curtas_home_lista")


# secoes de texto


@admin_required
def admin_secoes_home(request):
    secao_curtas = SecaoCurtas.objects.first()
    if not secao_curtas:
        secao_curtas = SecaoCurtas.objects.create(
            titulo="CURTAS EM DESTAQUE",
            subtitulo="Conheça algumas das obras produzidas pelos estudantes.",
        )

    secao_final = SecaoFinal.objects.first()
    if not secao_final:
        secao_final = SecaoFinal.objects.create(
            titulo="PRONTO PARA DAR VIDA ÀS SUAS IDEIAS?",
            subtitulo=(
                "Junte-se à Rede Miradas e comece a criar histórias."
            ),
            texto_botao="Conheça as trilhas",
            link_botao="/trilhas/",
        )

    if request.method == "POST":
        form_curtas = SecaoCurtasForm(
            request.POST, instance=secao_curtas, prefix="curtas"
        )
        form_final = SecaoFinalForm(
            request.POST, instance=secao_final, prefix="final"
        )
        if form_curtas.is_valid() and form_final.is_valid():
            form_curtas.save()
            form_final.save()
            messages.success(
                request,
                "Textos das seções da página inicial atualizados com sucesso!",
            )
            return redirect("admin_secoes_home")
    else:
        form_curtas = SecaoCurtasForm(instance=secao_curtas, prefix="curtas")
        form_final = SecaoFinalForm(instance=secao_final, prefix="final")

    return render(
        request,
        "rede_miradas/admin/secoes_home.html",
        {
            "form_curtas": form_curtas,
            "form_final": form_final,
        },
    )


# blog/noticias


@admin_required
def admin_noticias_lista(request):
    busca = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    filtro_status = request.GET.get("status", "").strip()

    noticias = Noticia.objects.all().order_by("-data_publicacao", "-id")

    if busca:
        noticias = noticias.filter(
            reduce(
                or_,
                [
                    Q(titulo__icontains=busca),
                    Q(resumo__icontains=busca),
                    Q(texto__icontains=busca),
                ],
            )
        )
    if categoria:
        noticias = noticias.filter(categoria=categoria)
    if filtro_status == "publicada":
        noticias = noticias.filter(publicada=True)
    elif filtro_status == "rascunho":
        noticias = noticias.filter(publicada=False)
    elif filtro_status == "destaque":
        noticias = noticias.filter(destaque=True)

    paginator = Paginator(noticias, 10)
    page_number = request.GET.get("pagina", 1)
    pagina_noticias = paginator.get_page(page_number)

    return render(
        request,
        "rede_miradas/admin/noticias_lista.html",
        {
            "pagina_noticias": pagina_noticias,
            "busca": busca,
            "categoria_selecionada": categoria,
            "status_selecionado": filtro_status,
            "categorias": Noticia.CATEGORIAS,
        },
    )


@admin_required
def admin_noticia_nova(request):
    if request.method == "POST":
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            if not noticia.slug:
                noticia.slug = slugify(noticia.titulo)
            noticia.save()
            messages.success(
                request, f'Notícia "{noticia.titulo}" cadastrada com sucesso!'
            )
            return redirect("admin_noticias_lista")
    else:
        form = NoticiaForm(
            initial={
                "publicada": True,
                "cor_fundo_destaque": "#3A1660",
            }
        )
    return render(
        request,
        "rede_miradas/admin/noticia_form.html",
        {"form": form, "titulo_acao": "Nova Notícia"},
    )


@admin_required
def admin_noticia_editar(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    if request.method == "POST":
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            noticia = form.save(commit=False)
            if not noticia.slug:
                noticia.slug = slugify(noticia.titulo)
            noticia.save()
            messages.success(
                request, f'Notícia "{noticia.titulo}" atualizada com sucesso!'
            )
            return redirect("admin_noticias_lista")
    else:
        form = NoticiaForm(instance=noticia)
    return render(
        request,
        "rede_miradas/admin/noticia_form.html",
        {
            "form": form,
            "noticia": noticia,
            "titulo_acao": f"Editar Notícia: {noticia.titulo}",
        },
    )


@admin_required
def admin_noticia_excluir(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    if request.method == "POST":
        titulo = noticia.titulo
        noticia.delete()
        messages.success(request, f'Notícia "{titulo}" excluída com sucesso.')
        return redirect("admin_noticias_lista")
    return render(
        request,
        "rede_miradas/admin/confirmar_exclusao.html",
        {
            "objeto": noticia,
            "tipo": "Notícia",
            "url_cancelar": "admin_noticias_lista",
        },
    )


@admin_required
def admin_noticia_toggle_pub(request, id):
    if not (
        request.user.is_superuser
        or request.user.has_perm("rede_miradas.pode_publicar_noticia")
    ):
        messages.error(
            request, "Você não possui permissão para publicar notícias."
        )
        return redirect("admin_noticias_lista")
    noticia = get_object_or_404(Noticia, id=id)
    noticia.publicada = not noticia.publicada
    noticia.save()
    status = "publicada" if noticia.publicada else "salva como rascunho"
    messages.info(request, f'Notícia "{noticia.titulo}" {status}.')
    return redirect("admin_noticias_lista")


@admin_required
def admin_noticia_toggle_destaque(request, id):
    if not (
        request.user.is_superuser
        or request.user.has_perm("rede_miradas.pode_destacar_noticia")
    ):
        messages.error(
            request, "Você não possui permissão para destacar notícias."
        )
        return redirect("admin_noticias_lista")
    noticia = get_object_or_404(Noticia, id=id)
    noticia.destaque = not noticia.destaque
    noticia.save()
    status = (
        "marcada como destaque" if noticia.destaque else "removida do destaque"
    )
    messages.info(request, f'Notícia "{noticia.titulo}" {status}.')
    return redirect("admin_noticias_lista")


# trilhas


@admin_required
def admin_trilhas_dashboard(request):
    hero = TrilhasHero.objects.first()
    faixa_itens = TrilhasFaixaItem.objects.order_by("ordem")
    cards = TrilhasCard.objects.annotate(
        total_unidades=Count("unidades", distinct=True),
        total_subtopicos=Count("subtopicos", distinct=True),
    ).order_by("ordem")

    context = {
        "hero": hero,
        "faixa_itens": faixa_itens,
        "cards": cards,
        "total_trilhas": cards.count(),
        "total_unidades": UnidadeTrilha.objects.count(),
        "total_topicos": TopicoUnidadeTrilha.objects.count(),
        "total_subtopicos": SubtopicoTrilha.objects.count(),
    }
    return render(
        request, "rede_miradas/admin/trilhas_dashboard.html", context
    )


@admin_required
def admin_trilhas_hero(request):
    hero = TrilhasHero.objects.first()
    if not hero:
        hero = TrilhasHero.objects.create(
            titulo="Bem-Vindo(a)",
            subtitulo="Aprenda produção audiovisual em módulos práticos.",
            mostrar_botao=True,
            texto_botao="Conheça as trilhas",
            link_botao="/trilhas/visao-geral/",
            cor_titulo="#FFFFFF",
            cor_subtitulo="#FFFFFF",
            cor_fundo_botao="#FFFFFF",
            cor_texto_botao="#0B0C10",
            cor_glow_1="#7C3AED",
            cor_glow_2="#22D3EE",
        )

    if request.method == "POST":
        form = TrilhasHeroForm(request.POST, request.FILES, instance=hero)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Configurações visuais do Hero das Trilhas atualizadas!",
            )
            return redirect("admin_trilhas_dashboard")
    else:
        form = TrilhasHeroForm(instance=hero)

    return render(
        request,
        "rede_miradas/admin/trilhas_hero.html",
        {"form": form, "hero": hero},
    )


# Faixa Informativa
@admin_required
def admin_trilhas_faixa_lista(request):
    itens = TrilhasFaixaItem.objects.order_by("ordem")
    return render(
        request,
        "rede_miradas/admin/trilhas_faixa_lista.html",
        {"itens": itens},
    )


@admin_required
def admin_trilhas_faixa_novo(request):
    if request.method == "POST":
        form = TrilhasFaixaItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item da faixa adicionado com sucesso!")
            return redirect("admin_trilhas_faixa_lista")
    else:
        form = TrilhasFaixaItemForm(
            initial={
                "ordem": TrilhasFaixaItem.objects.count() + 1,
                "ativo": True,
            }
        )
    return render(
        request,
        "rede_miradas/admin/trilhas_faixa_form.html",
        {"form": form, "titulo_acao": "Novo Item da Faixa"},
    )


@admin_required
def admin_trilhas_faixa_editar(request, id):
    item = get_object_or_404(TrilhasFaixaItem, id=id)
    if request.method == "POST":
        form = TrilhasFaixaItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item da faixa atualizado!")
            return redirect("admin_trilhas_faixa_lista")
    else:
        form = TrilhasFaixaItemForm(instance=item)
    return render(
        request,
        "rede_miradas/admin/trilhas_faixa_form.html",
        {"form": form, "item": item, "titulo_acao": "Editar Item da Faixa"},
    )


@admin_required
def admin_trilhas_faixa_excluir(request, id):
    item = get_object_or_404(TrilhasFaixaItem, id=id)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Item da faixa excluído.")
        return redirect("admin_trilhas_faixa_lista")
    return render(
        request,
        "rede_miradas/admin/confirmar_exclusao.html",
        {
            "objeto": item,
            "tipo": "Item da Faixa Informativa",
            "url_cancelar": "admin_trilhas_faixa_lista",
        },
    )


@admin_required
def admin_trilhas_faixa_toggle(request, id):
    item = get_object_or_404(TrilhasFaixaItem, id=id)
    item.ativo = not item.ativo
    item.save()
    messages.info(
        request, f"Item {'ativado' if item.ativo else 'desativado'}."
    )
    return redirect("admin_trilhas_faixa_lista")


# Cards das Trilhas
@admin_required
def admin_trilhas_cards_lista(request):
    cards = TrilhasCard.objects.annotate(
        total_unidades=Count("unidades", distinct=True),
        total_subtopicos=Count("subtopicos", distinct=True),
    ).order_by("ordem")
    return render(
        request,
        "rede_miradas/admin/trilhas_cards_lista.html",
        {"cards": cards},
    )


@admin_required
def admin_trilha_card_novo(request):
    if request.method == "POST":
        form = TrilhasCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            if not card.slug:
                card.slug = slugify(card.tag or card.titulo)
            card.save()
            messages.success(
                request, f'Trilha "{card.titulo}" criada com sucesso!'
            )
            return redirect("admin_trilhas_cards_lista")
    else:
        form = TrilhasCardForm(
            initial={
                "ativo": True,
                "ordem": TrilhasCard.objects.count() + 1,
                "cor_fundo_card": "#101535",
                "cor_borda_card": "#1E2659",
                "cor_glow": "#7C3AED",
                "cor_tag": "#94A3B8",
                "cor_titulo": "#FFFFFF",
                "cor_descricao": "#CBD5E1",
                "cor_fundo_botao": "#B94B61",
                "cor_texto_botao": "#FFFFFF",
                "cor_sidebar": "#8F3D4E",
                "cor_sidebar_topo": "#BA586C",
                "estilo_borda": "solid",
                "tag_negrito": True,
                "titulo_negrito": True,
                "mostrar_botao": True,
                "texto_botao": "Começar",
            }
        )
    return render(
        request,
        "rede_miradas/admin/trilha_card_form.html",
        {"form": form, "titulo_acao": "Nova Trilha de Aprendizagem"},
    )


@admin_required
def admin_trilha_card_editar(request, id):
    card = get_object_or_404(TrilhasCard, id=id)
    if request.method == "POST":
        form = TrilhasCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            card = form.save(commit=False)
            if not card.slug:
                card.slug = slugify(card.tag or card.titulo)
            card.save()
            messages.success(request, f'Trilha "{card.titulo}" atualizada!')
            return redirect("admin_trilhas_cards_lista")
    else:
        form = TrilhasCardForm(instance=card)
    return render(
        request,
        "rede_miradas/admin/trilha_card_form.html",
        {
            "form": form,
            "card": card,
            "titulo_acao": f"Editar Trilha: {card.titulo}",
        },
    )


@admin_required
def admin_trilha_card_excluir(request, id):
    card = get_object_or_404(TrilhasCard, id=id)
    if request.method == "POST":
        titulo = card.titulo
        card.delete()
        messages.success(request, f'Trilha "{titulo}" excluída com sucesso.')
        return redirect("admin_trilhas_cards_lista")
    return render(
        request,
        "rede_miradas/admin/confirmar_exclusao.html",
        {
            "objeto": card,
            "tipo": "Card de Trilha",
            "url_cancelar": "admin_trilhas_cards_lista",
        },
    )


@admin_required
def admin_trilha_card_toggle(request, id):
    if not (
        request.user.is_superuser
        or request.user.has_perm("rede_miradas.pode_gerenciar_trilhas")
    ):
        messages.error(
            request,
            "Você não possui permissão para gerenciar trilhas de aprendizagem.",
        )
        return redirect("admin_trilhas_cards_lista")
    card = get_object_or_404(TrilhasCard, id=id)
    card.ativo = not card.ativo
    card.save()
    messages.info(
        request,
        f'Trilha "{card.titulo}" {"ativada" if card.ativo else "desativada"}.',
    )
    return redirect("admin_trilhas_cards_lista")


# Unidades das Trilhas
@admin_required
def admin_unidades_lista(request):
    trilha_id = request.GET.get("trilha")
    unidades = (
        UnidadeTrilha.objects.select_related("trilha")
        .annotate(total_topicos=Count("topicos"))
        .order_by("trilha__ordem", "ordem", "numero")
    )

    if trilha_id:
        unidades = unidades.filter(trilha_id=trilha_id)

    trilhas = TrilhasCard.objects.order_by("ordem")
    return render(
        request,
        "rede_miradas/admin/unidades_lista.html",
        {
            "unidades": unidades,
            "trilhas": trilhas,
            "trilha_selecionada": int(trilha_id)
            if trilha_id and trilha_id.isdigit()
            else None,
        },
    )


@admin_required
def admin_unidade_nova(request):
    trilha_id = request.GET.get("trilha")
    if request.method == "POST":
        form = UnidadeTrilhaForm(request.POST)
        if form.is_valid():
            unidade = form.save()
            messages.success(
                request, f"Unidade {unidade.numero} ({unidade.titulo}) criada!"
            )
            return redirect(
                f"/painel/admin/trilhas/unidades/?trilha={unidade.trilha_id}"
            )
    else:
        initial = {"ativo": True, "numero": 1, "ordem": 1}
        if trilha_id and trilha_id.isdigit():
            initial["trilha"] = int(trilha_id)
            count = UnidadeTrilha.objects.filter(trilha_id=trilha_id).count()
            initial["numero"] = count + 1
            initial["ordem"] = count + 1
        form = UnidadeTrilhaForm(initial=initial)
    return render(
        request,
        "rede_miradas/admin/unidade_form.html",
        {"form": form, "titulo_acao": "Nova Unidade de Aprendizagem"},
    )


@admin_required
def admin_unidade_editar(request, id):
    unidade = get_object_or_404(UnidadeTrilha, id=id)
    if request.method == "POST":
        form = UnidadeTrilhaForm(request.POST, instance=unidade)
        if form.is_valid():
            unidade = form.save()
            messages.success(
                request,
                f"Unidade {unidade.numero} ({unidade.titulo}) atualizada!",
            )
            return redirect(
                f"/painel/admin/trilhas/unidades/?trilha={unidade.trilha_id}"
            )
    else:
        form = UnidadeTrilhaForm(instance=unidade)
    return render(
        request,
        "rede_miradas/admin/unidade_form.html",
        {
            "form": form,
            "unidade": unidade,
            "titulo_acao": f"Editar Unidade {unidade.numero}",
        },
    )


@admin_required
def admin_unidade_excluir(request, id):
    unidade = get_object_or_404(UnidadeTrilha, id=id)
    trilha_id = unidade.trilha_id
    if request.method == "POST":
        unidade.delete()
        messages.success(request, "Unidade excluída com sucesso.")
        return redirect(f"/painel/admin/trilhas/unidades/?trilha={trilha_id}")
    return render(
        request,
        "rede_miradas/admin/confirmar_exclusao.html",
        {
            "objeto": unidade,
            "tipo": "Unidade da Trilha",
            "url_cancelar": "admin_unidades_lista",
        },
    )


# Tópicos das Unidades
@admin_required
def admin_topicos_lista(request):
    unidade_id = request.GET.get("unidade")
    topicos = TopicoUnidadeTrilha.objects.select_related(
        "unidade", "unidade__trilha"
    ).order_by("unidade__trilha__ordem", "unidade__ordem", "ordem")
    if unidade_id:
        topicos = topicos.filter(unidade_id=unidade_id)

    unidades = UnidadeTrilha.objects.select_related("trilha").order_by(
        "trilha__ordem", "numero"
    )
    return render(
        request,
        "rede_miradas/admin/topicos_lista.html",
        {
            "topicos": topicos,
            "unidades": unidades,
            "unidade_selecionada": int(unidade_id)
            if unidade_id and unidade_id.isdigit()
            else None,
        },
    )


@admin_required
def admin_topico_novo(request):
    unidade_id = request.GET.get("unidade")
    if request.method == "POST":
        form = TopicoUnidadeTrilhaForm(request.POST)
        if form.is_valid():
            topico = form.save()
            messages.success(request, f'Tópico "{topico.titulo}" cadastrado!')
            return redirect(
                f"/painel/admin/trilhas/topicos/?unidade={topico.unidade_id}"
            )
    else:
        initial = {"ativo": True, "ordem": 1}
        if unidade_id and unidade_id.isdigit():
            initial["unidade"] = int(unidade_id)
            initial["ordem"] = (
                TopicoUnidadeTrilha.objects.filter(
                    unidade_id=unidade_id
                ).count()
                + 1
            )
        form = TopicoUnidadeTrilhaForm(initial=initial)
    return render(
        request,
        "rede_miradas/admin/topico_form.html",
        {"form": form, "titulo_acao": "Novo Conteúdo / Aula de Unidade"},
    )


@admin_required
def admin_topico_editar(request, id):
    topico = get_object_or_404(TopicoUnidadeTrilha, id=id)
    if request.method == "POST":
        form = TopicoUnidadeTrilhaForm(request.POST, instance=topico)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tópico "{topico.titulo}" atualizado!')
            return redirect(
                f"/painel/admin/trilhas/topicos/?unidade={topico.unidade_id}"
            )
    else:
        form = TopicoUnidadeTrilhaForm(instance=topico)
    return render(
        request,
        "rede_miradas/admin/topico_form.html",
        {
            "form": form,
            "topico": topico,
            "titulo_acao": f"Editar Tópico: {topico.titulo}",
        },
    )


@admin_required
def admin_topico_excluir(request, id):
    topico = get_object_or_404(TopicoUnidadeTrilha, id=id)
    unidade_id = topico.unidade_id
    if request.method == "POST":
        topico.delete()
        messages.success(request, "Tópico excluído com sucesso.")
        return redirect(f"/painel/admin/trilhas/topicos/?unidade={unidade_id}")
    return render(
        request,
        "rede_miradas/admin/confirmar_exclusao.html",
        {
            "objeto": topico,
            "tipo": "Tópico da Unidade",
            "url_cancelar": "admin_topicos_lista",
        },
    )


# Subtópicos Rápidos das Trilhas
@admin_required
def admin_subtopicos_lista(request):
    trilha_id = request.GET.get("trilha")
    subtopicos = SubtopicoTrilha.objects.select_related("trilha").order_by(
        "trilha__ordem", "ordem"
    )
    if trilha_id:
        subtopicos = subtopicos.filter(trilha_id=trilha_id)

    trilhas = TrilhasCard.objects.order_by("ordem")
    return render(
        request,
        "rede_miradas/admin/subtopicos_lista.html",
        {
            "subtopicos": subtopicos,
            "trilhas": trilhas,
            "trilha_selecionada": int(trilha_id)
            if trilha_id and trilha_id.isdigit()
            else None,
        },
    )


@admin_required
def admin_subtopico_novo(request):
    trilha_id = request.GET.get("trilha")
    if request.method == "POST":
        form = SubtopicoTrilhaForm(request.POST)
        if form.is_valid():
            sub = form.save()
            messages.success(request, f'Subtópico "{sub.titulo}" criado!')
            return redirect("admin_subtopicos_lista")
    else:
        initial = {"ativo": True, "ordem": 1}
        if trilha_id and trilha_id.isdigit():
            initial["trilha"] = int(trilha_id)
            initial["ordem"] = (
                SubtopicoTrilha.objects.filter(trilha_id=trilha_id).count() + 1
            )
        form = SubtopicoTrilhaForm(initial=initial)
    return render(
        request,
        "rede_miradas/admin/subtopico_form.html",
        {"form": form, "titulo_acao": "Novo Subtópico da Trilha"},
    )


@admin_required
def admin_subtopico_editar(request, id):
    sub = get_object_or_404(SubtopicoTrilha, id=id)
    if request.method == "POST":
        form = SubtopicoTrilhaForm(request.POST, instance=sub)
        if form.is_valid():
            form.save()
            messages.success(request, f'Subtópico "{sub.titulo}" atualizado!')
            return redirect("admin_subtopicos_lista")
    else:
        form = SubtopicoTrilhaForm(instance=sub)
    return render(
        request,
        "rede_miradas/admin/subtopico_form.html",
        {
            "form": form,
            "subtopico": sub,
            "titulo_acao": f"Editar Subtópico: {sub.titulo}",
        },
    )


@admin_required
def admin_subtopico_excluir(request, id):
    sub = get_object_or_404(SubtopicoTrilha, id=id)
    if request.method == "POST":
        sub.delete()
        messages.success(request, "Subtópico excluído com sucesso.")
        return redirect("admin_subtopicos_lista")
    return render(
        request,
        "rede_miradas/admin/confirmar_exclusao.html",
        {
            "objeto": sub,
            "tipo": "Subtópico da Trilha",
            "url_cancelar": "admin_subtopicos_lista",
        },
    )


# votação

@admin_required
def admin_votacao(request):
    curtas = CurtaVotacao.objects.annotate(
        total_votos=Count("votos")
    ).order_by("-total_votos", "ordem")

    total_geral_votos = Voto.objects.count()

    curtas_com_porcentagem = []
    for c in curtas:
        pct = (
            round((c.total_votos / total_geral_votos * 100), 1)
            if total_geral_votos > 0
            else 0
        )
        curtas_com_porcentagem.append(
            {
                "obj": c,
                "votos": c.total_votos,
                "porcentagem": pct,
            }
        )

    ultimos_votos = Voto.objects.select_related("usuario", "curta").order_by(
        "-data_voto"
    )[:10]

    return render(
        request,
        "rede_miradas/admin/votacao.html",
        {
            "curtas": curtas_com_porcentagem,
            "total_geral_votos": total_geral_votos,
            "total_curtas": curtas.count(),
            "ultimos_votos": ultimos_votos,
        },
    )


@admin_required
def admin_curta_votacao_novo(request):
    if request.method == "POST":
        form = CurtaVotacaoForm(request.POST, request.FILES)
        if form.is_valid():
            curta = form.save()
            messages.success(
                request, f'Curta "{curta.titulo}" cadastrado para a votação!'
            )
            return redirect("admin_votacao")
    else:
        form = CurtaVotacaoForm(
            initial={"ativo": True, "ordem": CurtaVotacao.objects.count() + 1}
        )
    return render(
        request,
        "rede_miradas/admin/curta_votacao_form.html",
        {"form": form, "titulo_acao": "Novo Curta para Votação"},
    )


@admin_required
def admin_curta_votacao_editar(request, id):
    curta = get_object_or_404(CurtaVotacao, id=id)
    if request.method == "POST":
        form = CurtaVotacaoForm(request.POST, request.FILES, instance=curta)
        if form.is_valid():
            form.save()
            messages.success(request, f'Curta "{curta.titulo}" atualizado!')
            return redirect("admin_votacao")
    else:
        form = CurtaVotacaoForm(instance=curta)
    return render(
        request,
        "rede_miradas/admin/curta_votacao_form.html",
        {
            "form": form,
            "curta": curta,
            "titulo_acao": f"Editar Curta: {curta.titulo}",
        },
    )


@admin_required
def admin_curta_votacao_excluir(request, id):
    curta = get_object_or_404(CurtaVotacao, id=id)
    if request.method == "POST":
        titulo = curta.titulo
        curta.delete()
        messages.success(request, f'Curta "{titulo}" excluído da votação.')
        return redirect("admin_votacao")
    return render(
        request,
        "rede_miradas/admin/confirmar_exclusao.html",
        {
            "objeto": curta,
            "tipo": "Curta em Votação",
            "url_cancelar": "admin_votacao",
        },
    )


@admin_required
def admin_curta_votacao_toggle(request, id):
    if not (
        request.user.is_superuser
        or request.user.has_perm("rede_miradas.pode_gerenciar_votacao")
    ):
        messages.error(
            request, "Você não possui permissão para gerenciar a votação."
        )
        return redirect("admin_votacao")
    curta = get_object_or_404(CurtaVotacao, id=id)
    curta.ativo = not curta.ativo
    curta.save()
    status_msg = "ativado" if curta.ativo else "desativado"
    messages.info(
        request,
        f'Curta "{curta.titulo}" {status_msg}.',
    )
    return redirect("admin_votacao")


# perfis


@admin_required
def admin_usuarios_lista(request):
    busca = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "").strip()

    usuarios = (
        User.objects.select_related("perfil")
        .prefetch_related("selos_conquistados")
        .order_by("-date_joined")
    )

    if busca:
        usuarios = usuarios.filter(
            reduce(
                or_,
                [
                    Q(username__icontains=busca),
                    Q(first_name__icontains=busca),
                    Q(last_name__icontains=busca),
                    Q(email__icontains=busca),
                    Q(perfil__escola__icontains=busca),
                    Q(perfil__grupo__icontains=busca),
                ],
            )
        )

    if tipo:
        usuarios = usuarios.filter(perfil__tipo=tipo)

    paginator = Paginator(usuarios, 15)
    pagina_usuarios = paginator.get_page(request.GET.get("pagina", 1))

    return render(
        request,
        "rede_miradas/admin/usuarios_lista.html",
        {
            "pagina_usuarios": pagina_usuarios,
            "busca": busca,
            "tipo_selecionado": tipo,
            "tipos_choices": Perfil.TIPO_CHOICES,
        },
    )


@admin_required
def admin_perfil_editar(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    perfil, _ = Perfil.objects.get_or_create(usuario=usuario)

    if request.method == "POST":
        form = PerfilAdminForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Perfil de "{usuario.username}" atualizado!'
            )
            return redirect("admin_usuarios_lista")
    else:
        form = PerfilAdminForm(instance=perfil)

    return render(
        request,
        "rede_miradas/admin/usuario_perfil_form.html",
        {
            "form": form,
            "usuario": usuario,
            "perfil": perfil,
        },
    )


@admin_required
def admin_usuario_excluir(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    # Não permitir que o administrador exclua a própria conta
    if request.user.id == usuario.id:
        messages.error(
            request,
            "Operação bloqueada: você não pode excluir sua própria conta!",
        )
        return redirect("admin_usuarios_lista")

    # Apenas superusuários podem excluir outros superusuários
    if usuario.is_superuser and not request.user.is_superuser:
        messages.error(
            request,
            "Apenas superadministradores podem excluir outros superadmins.",
        )
        return redirect("admin_usuarios_lista")

    if request.method == "POST":
        nome_exibicao = usuario.get_full_name() or usuario.username
        identificador = usuario.username
        usuario.delete()
        messages.success(
            request,
            f'Usuário "{nome_exibicao}" (@{identificador}) excluído.',
        )
        return redirect("admin_usuarios_lista")

    identificador = usuario.get_full_name() or usuario.username
    return render(
        request,
        "rede_miradas/admin/confirmar_exclusao.html",
        {
            "objeto": f"{identificador} (@{usuario.username})",
            "tipo": "Usuário e Perfil",
            "url_cancelar": "admin_usuarios_lista",
        },
    )
