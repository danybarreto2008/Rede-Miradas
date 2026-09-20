from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
#imports do login
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .forms import CadastroForm, LoginForm, CadastroProfessorForm
from .models import Perfil
from django.contrib.auth import authenticate

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
#views do login
def cadastro_aluno(request):

        if request.method == 'POST':

            form = CadastroForm(request.POST)

            if form.is_valid():

                usuario = form.save()

                Perfil.objects.create(usuario=usuario, tipo=Perfil.ALUNO)

                auth_login(request, usuario)

                return redirect('painel_aluno')

        else:

            form = CadastroForm()

        return render(request, 'rede_miradas/cadastro_aluno.html', {'form': form})


def cadastro_professor(request):

    if request.method == 'POST':

        form = CadastroProfessorForm(request.POST)

        if form.is_valid():

            usuario = form.save()

            Perfil.objects.create(usuario=usuario, tipo=Perfil.PROFESSOR)

            auth_login(request, usuario)

            return redirect('painel_professor')

    else:

        form = CadastroProfessorForm()

    return render(request, 'rede_miradas/cadastro_professor.html', {'form': form})

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

class LoginRedirecionadoView(LoginView):

    template_name = 'rede_miradas/login.html'
    authentication_form = LoginForm

    def get_success_url(self):

        usuario = self.request.user

        if hasattr(usuario, 'perfil') and usuario.perfil.tipo == Perfil.PROFESSOR:
            return reverse('painel_professor')

        if hasattr(usuario, 'perfil'):
            return reverse('painel_aluno')

        return reverse('home')

@login_required
def painel_aluno(request):
    return render(request, 'rede_miradas/painel_aluno.html')


@login_required
def painel_professor(request):
    return render(request, 'rede_miradas/painel_professor.html')



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

# View da página individual de uma notícia
def noticia_detalhe(request, slug):

    noticia = get_object_or_404(
        Noticia,
        slug=slug,
        publicada=True
    )

    # Notícias semelhantes: mesma categoria, publicadas, excluindo a atual
    noticias_semelhantes = Noticia.objects.filter(
        categoria=noticia.categoria,
        publicada=True
    ).exclude(
        id=noticia.id
    ).order_by('-data_publicacao', '-id')[:3]

    return render(
        request,
        "rede_miradas/noticia_detalhe.html",
        {
            'noticia': noticia,
            'noticias_semelhantes': noticias_semelhantes,
        }
    )