from functools import reduce
from operator import or_

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Prefetch, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db import IntegrityError, transaction

from .forms import MAX_FAVORITOS, PerfilForm, ProducaoFormSet
from .models import (
    BlocoApresentacao,
    Curta,
    CurtaVotacao,
    Destaque,
    NotaCurtaFavorito,
    Noticia,
    Perfil,
    SecaoCurtas,
    SecaoFinal,
    SeloConquistado,
    TopicoUnidadeTrilha,
    TrilhasCard,
    TrilhasFaixaItem,
    TrilhasHero,
    Voto,
    conceder_selo,
    TextosHome,
)
from .selos import SELOS
POSTS_POR_PAGINA = 6


@login_required
@require_POST
def confirmar_selo(request, conquista_id):
    SeloConquistado.objects.filter(
        id=conquista_id, usuario=request.user
    ).update(visualizado=True)
    return HttpResponse(status=204)


def _itens_busca():
    """
    Itens que a barra de busca do perfil encontra:
    páginas/funcionalidades do site e curtas em destaque.
    """
    itens = [
        {"tipo": "Página", "titulo": "Início", "url": reverse("home"), "icone": "bi-house-door"},
        {"tipo": "Página", "titulo": "Trilhas de aprendizagem", "url": reverse("inicial_trilhas"), "icone": "bi-mortarboard"},
        {"tipo": "Página", "titulo": "Notícias", "url": reverse("noticias"), "icone": "bi-newspaper"},
        {"tipo": "Página", "titulo": "Como tudo começou", "url": reverse("como_tudo_comecou"), "icone": "bi-clock-history"},
        {"tipo": "Função", "titulo": "Votação · Júri popular", "url": reverse("votacao"), "icone": "bi-star"},
        {"tipo": "Função", "titulo": "Meu perfil", "url": reverse("meu_perfil"), "icone": "bi-person"},
        {"tipo": "Função", "titulo": "Editar perfil", "url": reverse("editar_perfil"), "icone": "bi-pencil"},
    ]

    for curta in Curta.objects.filter(ativo=True).order_by("nome"):
        itens.append(
            {
                "tipo": "Curta",
                "titulo": curta.nome,
                "url": curta.link_youtube,
                "icone": "bi-film",
                "externo": True,
            }
        )

    return itens


def _selos_do_usuario(usuario):
    return [
        SELOS[c.selo]
        for c in SeloConquistado.objects.filter(usuario=usuario)
        if c.selo in SELOS
    ]


def _contexto_perfil(perfil, eh_dono):
    """Dados que a página de perfil mostra (meu perfil ou de outra pessoa)."""

    # curtas favoritos (até 4) com as estrelas que o usuário deu
    notas = dict(
        NotaCurtaFavorito.objects.filter(perfil=perfil).values_list(
            "curta_id", "nota"
        )
    )

    favoritos = [
        {"curta": curta, "nota": notas.get(curta.pk, 0)}
        for curta in perfil.curtas_favoritos.all()[:MAX_FAVORITOS]
    ]

    return {
        "perfil": perfil,
        "eh_dono": eh_dono,
        "favoritos": favoritos,
        "favoritos_vazios": range(MAX_FAVORITOS - len(favoritos)),
        "producoes": perfil.producoes.all(),
        "selos_conquistados": _selos_do_usuario(perfil.usuario),
        "busca_itens": _itens_busca(),
    }


@login_required
def meu_perfil(request):

    perfil = getattr(request.user, "perfil", None)

    if not perfil:
        messages.warning(
            request,
            "Perfil restrito a alunos e professores cadastrados via SUAP.",
        )
        return render(request, "rede_miradas/perfil_bloqueado.html")

    return render(
        request,
        "rede_miradas/meu_perfil.html",
        _contexto_perfil(perfil, eh_dono=True),
    )


@login_required
def ver_perfil(request, pk):
    """Perfil de outra pessoa (só para visualizar)."""

    perfil = get_object_or_404(
        Perfil.objects.select_related("usuario"),
        pk=pk,
        tipo__in=[Perfil.ALUNO, Perfil.PROFESSOR],
    )

    if perfil.usuario_id == request.user.id:
        return redirect("meu_perfil")

    return render(
        request,
        "rede_miradas/meu_perfil.html",
        _contexto_perfil(perfil, eh_dono=False),
    )


@login_required
def buscar_perfis(request):
    """Busca de perfis pelo nome (usada na barra de busca do perfil)."""

    termo = request.GET.get("q", "").strip()

    if len(termo) < 2:
        return JsonResponse({"perfis": []})

    consulta = Perfil.objects.select_related("usuario").filter(
        tipo__in=[Perfil.ALUNO, Perfil.PROFESSOR]
    ).exclude(usuario__first_name="")

    # cada palavra digitada precisa aparecer no nome ou no sobrenome
    for parte in termo.split()[:4]:
        consulta = consulta.filter(
            Q(usuario__first_name__icontains=parte)
            | Q(usuario__last_name__icontains=parte)
        )

    perfis = consulta.order_by("usuario__first_name")[:6]

    return JsonResponse(
        {
            "perfis": [
                {
                    "titulo": p.usuario.get_full_name(),
                    "detalhe": p.escola or p.get_tipo_display(),
                    "url": reverse("ver_perfil", args=[p.pk]),
                    "foto": p.foto.url if p.foto else "",
                }
                for p in perfis
            ]
        }
    )


@login_required
def editar_perfil(request):

    perfil = getattr(request.user, "perfil", None)

    if not perfil:
        messages.warning(
            request,
            "Perfil restrito a alunos e professores cadastrados via SUAP.",
        )
        return render(request, "rede_miradas/perfil_bloqueado.html")

    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        formset = ProducaoFormSet(
            request.POST,
            request.FILES,
            instance=perfil,
            prefix="producoes",
        )

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            # estrelas: guarda só dos curtas que continuam favoritos
            favoritos_ids = set(
                perfil.curtas_favoritos.values_list("pk", flat=True)
            )

            NotaCurtaFavorito.objects.filter(perfil=perfil).exclude(
                curta_id__in=favoritos_ids
            ).delete()

            for curta_id in favoritos_ids:
                try:
                    nota = int(request.POST.get(f"nota_{curta_id}", 0))
                except ValueError:
                    nota = 0

                NotaCurtaFavorito.objects.update_or_create(
                    perfil=perfil,
                    curta_id=curta_id,
                    defaults={"nota": max(0, min(5, nota))},
                )

            messages.success(request, "Seu perfil foi atualizado com sucesso!")
            return redirect("meu_perfil")

        messages.error(
            request,
            "Não foi possível salvar o perfil. Verifique os campos destacados abaixo.",
        )

    else:
        form = PerfilForm(instance=perfil)
        formset = ProducaoFormSet(instance=perfil, prefix="producoes")

    # curtas disponíveis para escolher como favoritos + estrelas já dadas
    if request.method == "POST":
        marcados = {
            int(valor)
            for valor in request.POST.getlist("curtas_favoritos")
            if valor.isdigit()
        }
        notas = {}
        for curta_id in marcados:
            try:
                notas[curta_id] = int(request.POST.get(f"nota_{curta_id}", 0))
            except ValueError:
                notas[curta_id] = 0
    else:
        marcados = set(perfil.curtas_favoritos.values_list("pk", flat=True))
        notas = dict(
            NotaCurtaFavorito.objects.filter(perfil=perfil).values_list(
                "curta_id", "nota"
            )
        )

    curtas_edicao = [
        {
            "curta": curta,
            "marcado": curta.pk in marcados,
            "nota": notas.get(curta.pk, 0),
        }
        for curta in Curta.objects.filter(ativo=True).order_by("ordem", "nome")
    ]

    return render(
        request,
        "rede_miradas/editar_perfil.html",
        {
            "form": form,
            "formset": formset,
            "perfil": perfil,
            "curtas_edicao": curtas_edicao,
            "max_favoritos": MAX_FAVORITOS,
            "selos_conquistados": _selos_do_usuario(request.user),
            "busca_itens": _itens_busca(),
        },
    )
@login_required
def votacao(request):

    curtas = CurtaVotacao.objects.filter(ativo=True).order_by("ordem")

    # 1 voto por e-mail (sempre minúsculo e sem espaços)
    email = (request.user.email or "").strip().lower()

    filtro_voto = Q(usuario=request.user)
    if email:
        filtro_voto |= Q(email=email)

    voto_usuario = (
        Voto.objects.select_related("curta").filter(filtro_voto).first()
    )

    if request.method == "POST":
        if voto_usuario:
            messages.warning(
                request,
                "Você já registrou seu voto nesta edição. Só é permitido um voto por e-mail.",
            )
            return redirect("votacao")

        if not email:
            messages.error(
                request,
                "Sua conta não tem e-mail cadastrado, por isso não foi possível registrar o voto.",
            )
            return redirect("votacao")

        curta_id = request.POST.get("curta_id", "")
        if not curta_id.isdigit():
            messages.error(request, "Curta inválido.")
            return redirect("votacao")

        curta = get_object_or_404(CurtaVotacao, id=curta_id, ativo=True)

        try:
            with transaction.atomic():
                Voto.objects.create(
                    usuario=request.user,
                    email=email,
                    curta=curta,
                )
        except IntegrityError:
            messages.warning(
                request,
                "Este e-mail já registrou um voto nesta edição.",
            )
            return redirect("votacao")

        conceder_selo(request.user, "primeiro-voto")
        messages.success(
            request,
            f"Seu voto no curta '{curta.titulo}' foi registrado com sucesso! Obrigado por participar.",
        )

        return redirect("votacao")

    return render(
        request,
        "rede_miradas/votacao.html",
        {
            "curtas": curtas,
            "voto_usuario": voto_usuario,
            "email_votante": email,
            "sem_email": not email,
        },
    )
@login_required
def redirecionar_apos_login(request):
    nome = request.user.first_name or request.user.username
    messages.success(request, f"Bem-vindo(a) à Rede Miradas, {nome}!")

    perfil = getattr(request.user, "perfil", None)

    if perfil and perfil.tipo == Perfil.PROFESSOR:
        return redirect("painel_professor")

    if perfil:
        return redirect("painel_aluno")

    return redirect("home")


def login_superadmin(request):
    from .admin_views import login_superadmin as admin_login_view

    return admin_login_view(request)


@login_required
def painel_aluno(request):
    return render(request, "rede_miradas/painel_aluno.html")


@login_required
def painel_professor(request):
    return render(request, "rede_miradas/painel_professor.html")


# página Comece por aqui
def home(request):

    destaques = Destaque.objects.filter(ativo=True).order_by("ordem")
    blocos = BlocoApresentacao.objects.filter(ativo=True).order_by("ordem")

    # Se ainda não existir, cria já com os textos padrão
    textos = TextosHome.objects.first() or TextosHome.objects.create()

    secao_curtas = SecaoCurtas.objects.first()
    curtas = Curta.objects.filter(ativo=True).order_by("ordem")
    secao_final = SecaoFinal.objects.first()

    return render(
        request,
        "rede_miradas/comeceporaqui.html",
        {
            "textos": textos,
            "secao_curtas": secao_curtas,
            "destaques": destaques,
            "blocos": blocos,
            "curtas": curtas,
            "secao_final": secao_final,
        },
    )


# página de notícias
def pagina_noticias(request):

    noticias_publicadas = Noticia.objects.filter(publicada=True)

    destaque = (
        noticias_publicadas.filter(destaque=True)
        .order_by("-data_publicacao", "-id")
        .first()
    )

    disponiveis = noticias_publicadas
    if destaque:
        disponiveis = disponiveis.exclude(id=destaque.id)

    destaques_secundarios = disponiveis.filter(
        destaque_secundario=True
    ).order_by("-data_publicacao", "-id")

    disponiveis = disponiveis.exclude(
        id__in=destaques_secundarios.values_list("id", flat=True)
    )

    busca = request.GET.get("q", "").strip()

    if busca:
        disponiveis = disponiveis.filter(
            reduce(
                or_,
                [
                    Q(titulo__icontains=busca),
                    Q(resumo__icontains=busca),
                    Q(texto__icontains=busca),
                ],
            )
        )
        if not disponiveis.exists():
            messages.info(
                request, f"Nenhuma notícia encontrada para a busca '{busca}'."
            )

    disponiveis = disponiveis.order_by("-data_publicacao", "-id")

    ids_ultimas = list(disponiveis.values_list("id", flat=True)[:3])
    noticias = disponiveis.filter(id__in=ids_ultimas).order_by(
        "-data_publicacao", "-id"
    )

    outros = disponiveis.exclude(id__in=ids_ultimas)

    paginator = Paginator(outros, POSTS_POR_PAGINA)
    pagina_outros = paginator.get_page(1)

    return render(
        request,
        "rede_miradas/noticias.html",
        {
            "destaque": destaque,
            "destaques_secundarios": destaques_secundarios,
            "noticias": noticias,
            "pagina_outros": pagina_outros,
            "busca": busca,
        },
    )

def carregar_mais_noticias(request):

    noticias_publicadas = Noticia.objects.filter(publicada=True)

    destaque = (
        noticias_publicadas.filter(destaque=True)
        .order_by("-data_publicacao", "-id")
        .first()
    )

    disponiveis = noticias_publicadas
    if destaque:
        disponiveis = disponiveis.exclude(id=destaque.id)

    destaques_secundarios_ids = disponiveis.filter(
        destaque_secundario=True
    ).values_list("id", flat=True)

    disponiveis = disponiveis.exclude(id__in=destaques_secundarios_ids)

    busca = request.GET.get("q", "").strip()
    if busca:
        disponiveis = disponiveis.filter(
            reduce(
                or_,
                [
                    Q(titulo__icontains=busca),
                    Q(resumo__icontains=busca),
                    Q(texto__icontains=busca),
                ],
            )
        )

    disponiveis = disponiveis.order_by("-data_publicacao", "-id")

    ids_ultimas = list(disponiveis.values_list("id", flat=True)[:3])

    outros = disponiveis.exclude(id__in=ids_ultimas)

    numero_pagina = request.GET.get("pagina", 1)
    paginator = Paginator(outros, POSTS_POR_PAGINA)

    try:
        pagina = paginator.page(numero_pagina)
    except EmptyPage:
        return HttpResponse()

    return render(
        request,
        "rede_miradas/_cards_outros_posts.html",
        {"pagina_outros": pagina},
    )


# página individual de uma notícia
def noticia_detalhe(request, slug):

    noticia = get_object_or_404(Noticia, slug=slug, publicada=True)

    da_mesma_categoria = list(
        Noticia.objects.filter(categoria=noticia.categoria, publicada=True)
        .exclude(id=noticia.id)
        .order_by("-data_publicacao", "-id")[:3]
    )

    if len(da_mesma_categoria) < 3:
        ids_ja_escolhidos = [n.id for n in da_mesma_categoria] + [noticia.id]

        faltam = 3 - len(da_mesma_categoria)

        outras = (
            Noticia.objects.filter(publicada=True)
            .exclude(id__in=ids_ja_escolhidos)
            .order_by("-data_publicacao", "-id")[:faltam]
        )

        noticias_semelhantes = da_mesma_categoria + list(outras)

    else:
        noticias_semelhantes = da_mesma_categoria

    return render(
        request,
        "rede_miradas/noticia_detalhe.html",
        {
            "noticia": noticia,
            "noticias_semelhantes": noticias_semelhantes,
        },
    )


# página inicial das Trilhas de Aprendizagem
def inicial_trilhas(request):
    hero = TrilhasHero.objects.first()
    itens_faixa = TrilhasFaixaItem.objects.filter(ativo=True).order_by("ordem")
    cards = (
        TrilhasCard.objects.filter(ativo=True)
        .prefetch_related("subtopicos")
        .order_by("ordem")
    )

    return render(
        request,
        "rede_miradas/inicial_trilhas.html",
        {
            "hero": hero,
            "itens_faixa": itens_faixa,
            "cards": cards,
        },
    )


# visão geral das trilhas 
def trilhas_visao_geral(request):
    cards = list(
        TrilhasCard.objects.filter(ativo=True)
        .prefetch_related("subtopicos")
        .order_by("ordem")
    )
    if hasattr(request, "user") and request.user.is_authenticated:
        progresso_trilhas = request.session.get("progresso_trilhas", {})
        for card in cards:
            card.subtopico_ativo = progresso_trilhas.get(card.slug)
    else:
        for card in cards:
            card.subtopico_ativo = None

    return render(
        request,
        "rede_miradas/trilhas_visão_geral.html",
        {
            "cards": cards,
        },
    )


def trilha_detalhe(request, slug=None):
    if not slug:
        trilha = TrilhasCard.objects.filter(
            reduce(
                or_,
                [
                    Q(slug="inscricao-das-equipes"),
                    Q(titulo__icontains="inscrição"),
                    Q(tag__icontains="inscrição"),
                ],
            )
        ).first()
        if not trilha:
            trilha = (
                TrilhasCard.objects.filter(ativo=True)
                .order_by("ordem")
                .first()
            )
    else:
        trilha = get_object_or_404(TrilhasCard, slug=slug, ativo=True)

    if not trilha:
        messages.warning(
            request, "A trilha de aprendizagem solicitada não foi encontrada."
        )
        return redirect("trilhas_visao_geral")

    unidades = (
        trilha.unidades.filter(ativo=True)
        .prefetch_related(
            Prefetch(
                "topicos",
                queryset=TopicoUnidadeTrilha.objects.filter(
                    ativo=True
                ).order_by("ordem"),
            )
        )
        .order_by("ordem", "numero")
    )

    proxima_trilha = (
        TrilhasCard.objects.filter(ativo=True, ordem__gt=trilha.ordem)
        .order_by("ordem")
        .first()
    )

    trilha_anterior = (
        TrilhasCard.objects.filter(ativo=True, ordem__lt=trilha.ordem)
        .order_by("-ordem")
        .first()
    )

    is_auth = hasattr(request, "user") and request.user.is_authenticated
    progresso_trilhas = (
        request.session.get("progresso_trilhas", {}) if is_auth else {}
    )
    unidade_param = request.GET.get("unidade")
    if unidade_param and str(unidade_param).isdigit():
        unidade_atual_num = int(unidade_param)
    else:
        unidade_atual_num = (
            progresso_trilhas.get(trilha.slug, 1) if is_auth else 1
        )

    if is_auth:
        progresso_trilhas[trilha.slug] = unidade_atual_num
        request.session["progresso_trilhas"] = progresso_trilhas
        subtopico_titulo = ""
        subtopicos = list(trilha.subtopicos.filter(ativo=True).order_by("ordem"))
        if 1 <= unidade_atual_num <= len(subtopicos):
            subtopico_titulo = subtopicos[unidade_atual_num - 1].titulo
        else:
            un_obj = unidades.filter(numero=unidade_atual_num).first()
            if un_obj:
                subtopico_titulo = un_obj.titulo

        url_com_unidade = (
            f"/trilhas/{trilha.slug}/?unidade={unidade_atual_num}#unidade-{unidade_atual_num}"
            if trilha.slug
            else "/trilhas/visao-geral/"
        )

        item_sessao = {
            "id": trilha.id,
            "slug": trilha.slug or "",
            "tag": trilha.tag or "",
            "titulo": trilha.titulo or "",
            "subtopico_titulo": subtopico_titulo,
            "unidade_atual": unidade_atual_num,
            "url": url_com_unidade,
            "total_unidades": unidades.count(),
            "capa_url": trilha.imagem_capa.url if trilha.imagem_capa else "",
        }
        request.session["ultima_trilha"] = item_sessao

        historico = request.session.get("historico_trilhas", [])
        historico = [h for h in historico if h.get("id") != trilha.id]
        historico.insert(0, item_sessao)
        request.session["historico_trilhas"] = historico[:5]
        request.session.modified = True

    return render(
        request,
        "rede_miradas/trilha_detalhe.html",
        {
            "trilha": trilha,
            "unidades": unidades,
            "total_unidades": unidades.count(),
            "unidade_atual_num": unidade_atual_num,
            "trilha_anterior": trilha_anterior,
            "proxima_trilha": proxima_trilha,
        },
    )


def salvar_progresso_trilha(request):
    if not (hasattr(request, "user") and request.user.is_authenticated):
        return HttpResponse(status=204)
    slug = request.GET.get("slug") or request.POST.get("slug")
    unidade = request.GET.get("unidade") or request.POST.get("unidade")
    if slug and unidade and str(unidade).isdigit():
        unidade_num = int(unidade)
        progresso_trilhas = request.session.get("progresso_trilhas", {})
        progresso_trilhas[slug] = unidade_num
        request.session["progresso_trilhas"] = progresso_trilhas

        ultima = request.session.get("ultima_trilha")
        if ultima and ultima.get("slug") == slug:
            ultima["unidade_atual"] = unidade_num
            ultima["url"] = f"/trilhas/{slug}/?unidade={unidade_num}#unidade-{unidade_num}"
            trilha = TrilhasCard.objects.filter(slug=slug).first()
            if trilha:
                subtopicos = list(trilha.subtopicos.filter(ativo=True).order_by("ordem"))
                if 1 <= unidade_num <= len(subtopicos):
                    ultima["subtopico_titulo"] = subtopicos[unidade_num - 1].titulo
                else:
                    un = trilha.unidades.filter(numero=unidade_num).first()
                    if un:
                        ultima["subtopico_titulo"] = un.titulo
            request.session["ultima_trilha"] = ultima

        request.session.modified = True
        return HttpResponse(status=204)
    return HttpResponse(status=400)


def limpar_historico_trilhas(request):
    request.session.pop("historico_trilhas", None)
    request.session.pop("ultima_trilha", None)
    request.session.pop("progresso_trilhas", None)
    request.session.modified = True
    messages.info(
        request, "Seu histórico de navegação nas trilhas foi limpo com sucesso."
    )
    return redirect(request.META.get("HTTP_REFERER", "trilhas_visao_geral"))


def trilha_inscricao_equipes(request):
    return trilha_detalhe(request, slug="inscricao-das-equipes")


#Como Tudo Começou
def como_tudo_comecou(request):
    return render(request, "rede_miradas/como_tudo_comecou.html")

