from functools import reduce
from operator import or_

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Prefetch, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PerfilForm
from .models import (
    BlocoApresentacao,
    Curta,
    CurtaVotacao,
    Destaque,
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


@login_required
def meu_perfil(request):

    perfil = getattr(request.user, "perfil", None)

    if not perfil:
        return render(request, "rede_miradas/perfil_bloqueado.html")

    favoritos = perfil.curtas_favoritos.all()

    voto = Voto.objects.filter(usuario=request.user).first()

    selos = []

    selos.append(
        {
            "icone": "bi-stars",
            "nome": "Primeiro passo",
            "descricao": "Você entrou para a Rede Miradas.",
            "cor": "rosa",
        }
    )

    if favoritos.count() >= 3:
        selos.append(
            {
                "icone": "bi-film",
                "nome": "Olhar de cinema",
                "descricao": "Você adicionou 3 ou mais curtas aos favoritos.",
                "cor": "roxo",
            }
        )

    if perfil.nome_curta_participou:
        selos.append(
            {
                "icone": "bi-pencil",
                "nome": "Mão na massa",
                "descricao": "Você participou de uma produção audiovisual.",
                "cor": "azul",
            }
        )

    if voto:
        selos.append(
            {
                "icone": "bi-star",
                "nome": "Júri popular",
                "descricao": "Você participou da votação.",
                "cor": "verde",
            }
        )

    selos_conquistados = [
        SELOS[c.selo]
        for c in SeloConquistado.objects.filter(usuario=request.user)
        if c.selo in SELOS
    ]

    return render(
        request,
        "rede_miradas/meu_perfil.html",
        {
            "perfil": perfil,
            "favoritos": favoritos,
            "selos": selos,
            "selos_conquistados": selos_conquistados,
            "voto": voto,
        },
    )


@login_required
def editar_perfil(request):

    perfil = getattr(request.user, "perfil", None)

    if not perfil:
        return render(request, "rede_miradas/perfil_bloqueado.html")

    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil)

        if form.is_valid():
            form.save()

            return redirect("meu_perfil")

    else:
        form = PerfilForm(instance=perfil)

    return render(
        request,
        "rede_miradas/editar_perfil.html",
        {
            "form": form,
            "perfil": perfil,
        },
    )


@login_required
def votacao(request):

    curtas = CurtaVotacao.objects.filter(ativo=True).order_by("ordem")

    voto_usuario = Voto.objects.filter(usuario=request.user).first()

    if request.method == "POST" and not voto_usuario:
        curta_id = request.POST.get("curta_id")
        curta = get_object_or_404(CurtaVotacao, id=curta_id)

        Voto.objects.create(usuario=request.user, curta=curta)
        conceder_selo(request.user, "primeiro-voto")

        return redirect("votacao")

    return render(
        request,
        "rede_miradas/votacao.html",
        {
            "curtas": curtas,
            "voto_usuario": voto_usuario,
        },
    )


@login_required
def redirecionar_apos_login(request):

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

    secao_curtas = SecaoCurtas.objects.first()

    curtas = Curta.objects.filter(ativo=True).order_by("ordem")

    secao_final = SecaoFinal.objects.first()

    return render(
        request,
        "rede_miradas/comeceporaqui.html",
        {
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
    progresso_trilhas = request.session.get("progresso_trilhas", {})
    for card in cards:
        card.subtopico_ativo = progresso_trilhas.get(card.slug)

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

    progresso_trilhas = request.session.get("progresso_trilhas", {})
    unidade_param = request.GET.get("unidade")
    if unidade_param and str(unidade_param).isdigit():
        unidade_atual_num = int(unidade_param)
    else:
        unidade_atual_num = progresso_trilhas.get(trilha.slug, 1)

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
    return redirect(request.META.get("HTTP_REFERER", "trilhas_visao_geral"))


def trilha_inscricao_equipes(request):
    return trilha_detalhe(request, slug="inscricao-das-equipes")


#Como Tudo Começou
def como_tudo_comecou(request):
    return render(request, "rede_miradas/como_tudo_comecou.html")

