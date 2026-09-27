from .models import SeloConquistado
from .selos import SELOS


def selo_pendente(request):
    if request.user.is_authenticated:
        conquista = SeloConquistado.objects.filter(
            usuario=request.user,
            visualizado=False
        ).first()

        if conquista and conquista.selo in SELOS:
            return {
                'selo_pendente': conquista,
                'selo_pendente_info': SELOS[conquista.selo],
            }

    return {'selo_pendente': None, 'selo_pendente_info': None}