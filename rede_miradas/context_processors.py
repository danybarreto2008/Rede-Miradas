from .models import SeloConquistado
from .selos import SELOS


def selo_pendente(request):
    if request.user.is_authenticated:
        conquista = SeloConquistado.objects.filter(  # type: ignore
            usuario=request.user,
            visualizado=False
        ).first()

        if conquista and conquista.selo in SELOS:
            return {
                'selo_pendente': conquista,
                'selo_pendente_info': SELOS[conquista.selo],
            }

    return {'selo_pendente': None, 'selo_pendente_info': None}


def historico_trilhas(request):
    return {
        'ultima_trilha_acessada': request.session.get('ultima_trilha'),
        'historico_trilhas': request.session.get('historico_trilhas', []),
        'progresso_trilhas': request.session.get('progresso_trilhas', {}),
    }

