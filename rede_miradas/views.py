from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Destaque, Noticia


# View da página "Comece por aqui"
def home(request):

    destaques = Destaque.objects.filter(
        ativo=True
    ).order_by('ordem')

    return render(
        request,
        "rede_miradas/comeceporaqui.html",
        {
            'destaques': destaques
        }
    )


# View da página de notícias
def pagina_noticias(request):

    # Busca somente as notícias publicadas
    noticias_publicadas = Noticia.objects.filter(
        publicada=True
    )

    # Busca a notícia que foi marcada como destaque
    destaque = noticias_publicadas.filter(
        destaque=True
    ).order_by('-data_publicacao').first()

    # Começa com todas as notícias publicadas
    noticias = noticias_publicadas

    # Se existe uma notícia em destaque,
    # ela não aparece novamente nas últimas notícias
    if destaque:
        noticias = noticias.exclude(
            id=destaque.id
        )

    # Busca digitada pelo usuário
    busca = request.GET.get('q', '').strip()

    # Se o usuário pesquisou alguma coisa,
    # procura no título, resumo ou texto da notícia
    if busca:
        noticias = noticias.filter(
            Q(titulo__icontains=busca) |
            Q(resumo__icontains=busca) |
            Q(texto__icontains=busca)
        )

    # Notícias mais recentes aparecem primeiro
    noticias = noticias.order_by(
        '-data_publicacao'
    )

    return render(
        request,
        "rede_miradas/noticias.html",
        {
            'destaque': destaque,
            'noticias': noticias,
            'busca': busca,
        }
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