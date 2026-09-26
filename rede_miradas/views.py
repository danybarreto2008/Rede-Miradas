from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
#imports do login
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Perfil
from django.contrib.auth.decorators import login_required
from .forms import PerfilForm

from .models import (
    Destaque,
    Noticia,
    BlocoApresentacao,
    Curta,
    SecaoCurtas,
    SecaoFinal,
    TrilhasHero,
    TrilhasFaixaItem,
    TrilhasCard,
    Voto,
    CurtaVotacao
)

POSTS_POR_PAGINA = 6
@login_required
def meu_perfil(request):

    perfil = getattr(request.user, 'perfil', None)

    if not perfil:
        return render(
            request,
            'rede_miradas/perfil_bloqueado.html'
        )

    favoritos = perfil.curtas_favoritos.all()

    voto = Voto.objects.filter(
        usuario=request.user
    ).first()

    selos = []

    selos.append({
        'icone': 'bi-stars',
        'nome': 'Primeiro passo',
        'descricao': 'Você entrou para a Rede Miradas.',
        'cor': 'rosa'
    })

    if favoritos.count() >= 3:
        selos.append({
            'icone': 'bi-film',
            'nome': 'Olhar de cinema',
            'descricao': 'Você adicionou 3 ou mais curtas aos favoritos.',
            'cor': 'roxo'
        })

    if perfil.nome_curta_participou:
        selos.append({
            'icone': 'bi-pencil',
            'nome': 'Mão na massa',
            'descricao': 'Você participou de uma produção audiovisual.',
            'cor': 'azul'
        })

    if voto:
        selos.append({
            'icone': 'bi-star',
            'nome': 'Júri popular',
            'descricao': 'Você participou da votação.',
            'cor': 'verde'
        })

    return render(
        request,
        'rede_miradas/meu_perfil.html',
        {
            'perfil': perfil,
            'favoritos': favoritos,
            'selos': selos,
            'voto': voto,
        }
    )

@login_required
def editar_perfil(request):

    perfil = getattr(request.user, 'perfil', None)

    if not perfil:
        return render(
            request,
            'rede_miradas/perfil_bloqueado.html'
        )

    if request.method == 'POST':

        form = PerfilForm(
            request.POST,
            request.FILES,
            instance=perfil
        )

        if form.is_valid():
            form.save()

            return redirect('meu_perfil')

    else:

        form = PerfilForm(instance=perfil)

    return render(
        request,
        'rede_miradas/editar_perfil.html',
        {
            'form': form,
            'perfil': perfil,
        }
    )

@login_required
def votacao(request):

    curtas = CurtaVotacao.objects.filter(
        ativo=True
    ).order_by('ordem')

    voto_usuario = Voto.objects.filter(usuario=request.user).first()

    if request.method == 'POST' and not voto_usuario:

        curta_id = request.POST.get('curta_id')
        curta = get_object_or_404(CurtaVotacao, id=curta_id)

        Voto.objects.create(usuario=request.user, curta=curta)

        return redirect('votacao')

    return render(request, 'rede_miradas/votacao.html', {
        'curtas': curtas,
        'voto_usuario': voto_usuario,
})

@login_required
def redirecionar_apos_login(request):

    perfil = getattr(request.user, 'perfil', None)

    if perfil and perfil.tipo == Perfil.PROFESSOR:
        return redirect('painel_professor')

    if perfil:
        return redirect('painel_aluno')

    return redirect('home')

def login_superadmin(request):

    erro = None

    if request.method == 'POST':

        identificador = request.POST.get('username')
        senha = request.POST.get('password')

        usuario = authenticate(request, username=identificador, password=senha)

        if usuario is not None and usuario.is_superuser:

            auth_login(request, usuario)

            return redirect('admin:index')

        erro = 'Credenciais inválidas ou sem permissão de superadministrador.'

    return render(request, 'rede_miradas/login_superadmin.html', {'erro': erro})


@login_required
def painel_aluno(request):
    return render(request, 'rede_miradas/painel_aluno.html')


@login_required
def painel_professor(request):
    return render(request, 'rede_miradas/painel_professor.html')


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

    # Primeiro tenta notícias da mesma categoria
    da_mesma_categoria = list(
        Noticia.objects.filter(
            categoria=noticia.categoria,
            publicada=True
        ).exclude(
            id=noticia.id
        ).order_by('-data_publicacao', '-id')[:3]
    )

    # Se não tiver 3 da mesma categoria, completa com outras notícias
    # recentes do site (de qualquer categoria)
    if len(da_mesma_categoria) < 3:

        ids_ja_escolhidos = [n.id for n in da_mesma_categoria] + [noticia.id]

        faltam = 3 - len(da_mesma_categoria)

        outras = Noticia.objects.filter(
            publicada=True
        ).exclude(
            id__in=ids_ja_escolhidos
        ).order_by('-data_publicacao', '-id')[:faltam]

        noticias_semelhantes = da_mesma_categoria + list(outras)

    else:
        noticias_semelhantes = da_mesma_categoria

    return render(
        request,
        "rede_miradas/noticia_detalhe.html",
        {
            'noticia': noticia,
            'noticias_semelhantes': noticias_semelhantes,
        }
    )


# View da página inicial das Trilhas de Aprendizagem
def inicial_trilhas(request):
    hero = TrilhasHero.objects.first()
    itens_faixa = TrilhasFaixaItem.objects.filter(ativo=True).order_by('ordem')
    cards = TrilhasCard.objects.filter(ativo=True).prefetch_related('subtopicos').order_by('ordem')

    return render(
        request,
        "rede_miradas/inicial_trilhas.html",
        {
            'hero': hero,
            'itens_faixa': itens_faixa,
            'cards': cards,
        }
    )


# View da página de visão geral das trilhas (Layout Substack Figma)
def trilhas_visao_geral(request):
    cards = TrilhasCard.objects.filter(ativo=True).prefetch_related('subtopicos').order_by('ordem')

    return render(
        request,
        "rede_miradas/trilhas_visão_geral.html",
        {
            'cards': cards,
        }
    )