from django.shortcuts import render

from .models import Destaque


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