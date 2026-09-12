from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage

from .models import (
    Destaque,
    Noticia,
    BlocoApresentacao,
    Curta,
    SecaoCurtas,
    SecaoFinal,
    TrilhasHero,
    TrilhasFaixaItem,
    TrilhasCard
)

POSTS_POR_PAGINA = 6


# View da página "Comece por aqui"
def home(request):

    destaques = Destaque.objects.filter(
        ativo=True
    ).order_by('ordem')

    blocos = BlocoApresentacao.objects.filter(
        ativo=True
    ).order_by('ordem')

    secao_curtas = SecaoCurtas.objects.first()

    curtas = Curta.objects.filter(
        ativo=True
    ).order_by('ordem')

    secao_final = SecaoFinal.objects.first()

    return render(
        request,
        "rede_miradas/comeceporaqui.html",
        {
            'secao_curtas': secao_curtas,
            'destaques': destaques,
            'blocos': blocos,
            'curtas': curtas,
            'secao_final': secao_final,
        }
    )


# View da página de notícias
def pagina_noticias(request):

    noticias_publicadas = Noticia.objects.filter(publicada=True)

    # Notícia em destaque principal
    destaque = noticias_publicadas.filter(
        destaque=True
    ).order_by('-data_publicacao', '-id').first()

    disponiveis = noticias_publicadas
    if destaque:
        disponiveis = disponiveis.exclude(id=destaque.id)

    # Destaques secundários
    destaques_secundarios = disponiveis.filter(
        destaque_secundario=True
    ).order_by('-data_publicacao', '-id')

    disponiveis = disponiveis.exclude(
        id__in=destaques_secundarios.values_list('id', flat=True)
    )

    busca = request.GET.get('q', '').strip()

    if busca:
        disponiveis = disponiveis.filter(
            Q(titulo__icontains=busca) |
            Q(resumo__icontains=busca) |
            Q(texto__icontains=busca)
        )

    disponiveis = disponiveis.order_by('-data_publicacao', '-id')

    # As 3 mais recentes vão para a seção "Últimas notícias"
    ids_ultimas = list(disponiveis.values_list('id', flat=True)[:3])
    noticias = disponiveis.filter(id__in=ids_ultimas).order_by('-data_publicacao', '-id')

    # O resto vai para a seção "Outros posts", paginada
    outros = disponiveis.exclude(id__in=ids_ultimas)

    paginator = Paginator(outros, POSTS_POR_PAGINA)
    pagina_outros = paginator.get_page(1)

    return render(
        request,
        "rede_miradas/noticias.html",
        {
            'destaque': destaque,
            'destaques_secundarios': destaques_secundarios,
            'noticias': noticias,
            'pagina_outros': pagina_outros,
            'busca': busca,
        }
    )


# View que devolve mais posts em HTML puro, usada pelo botão "Carregar mais"
def carregar_mais_noticias(request):

    noticias_publicadas = Noticia.objects.filter(publicada=True)

    destaque = noticias_publicadas.filter(
        destaque=True
    ).order_by('-data_publicacao', '-id').first()

    disponiveis = noticias_publicadas
    if destaque:
        disponiveis = disponiveis.exclude(id=destaque.id)

    destaques_secundarios_ids = disponiveis.filter(
        destaque_secundario=True
    ).values_list('id', flat=True)

    disponiveis = disponiveis.exclude(id__in=destaques_secundarios_ids)

    busca = request.GET.get('q', '').strip()
    if busca:
        disponiveis = disponiveis.filter(
            Q(titulo__icontains=busca) |
            Q(resumo__icontains=busca) |
            Q(texto__icontains=busca)
        )

    disponiveis = disponiveis.order_by('-data_publicacao', '-id')

    # IDs das 3 notícias que já aparecem em "Últimas notícias"
    ids_ultimas = list(disponiveis.values_list('id', flat=True)[:3])

    outros = disponiveis.exclude(id__in=ids_ultimas)

    numero_pagina = request.GET.get('pagina', 1)
    paginator = Paginator(outros, POSTS_POR_PAGINA)

    try:
        pagina = paginator.page(numero_pagina)
    except EmptyPage:
        # Não existe mais nenhuma página além dessa —
        # devolve vazio para o botão "Carregar mais" saber que acabou
        return HttpResponse('')

    return render(
        request,
        "rede_miradas/_cards_outros_posts.html",
        {'pagina_outros': pagina}
    )


# View da página individual de uma notícia
def noticia_detalhe(request, slug):

    noticia = get_object_or_404(
        Noticia,
        slug=slug,
        publicada=True
    )

    return render(
        request,
        "rede_miradas/noticia_detalhe.html",
        {
            'noticia': noticia
        }
    )


# View da página inicial das Trilhas de Aprendizagem
def inicial_trilhas(request):
    hero = TrilhasHero.objects.first()
    itens_faixa = TrilhasFaixaItem.objects.filter(ativo=True).order_by('ordem')
    cards = TrilhasCard.objects.filter(ativo=True).order_by('ordem')

    return render(
        request,
        "rede_miradas/inicial_trilhas.html",
        {
            'hero': hero,
            'itens_faixa': itens_faixa,
            'cards': cards,
        }
    )


# View da página de visão geral das trilhas
def trilhas_visao_geral(request):
    return render(
        request,
        "rede_miradas/trilhas_visão_geral.html"
    )