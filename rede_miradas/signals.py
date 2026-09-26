from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from .models import Perfil


@receiver(pre_social_login)
def criar_perfil_ao_logar_suap(sender, request, sociallogin, **kwargs):

    if not sociallogin.is_existing:
        return

    usuario = sociallogin.user

    if hasattr(usuario, 'perfil'):
        return

    dados = sociallogin.account.extra_data

    tipo_vinculo = dados.get('tipo_vinculo', '').lower()

    if 'servidor' in tipo_vinculo or 'professor' in tipo_vinculo or 'docente' in tipo_vinculo:
        tipo = Perfil.PROFESSOR
    else:
        tipo = Perfil.ALUNO

    Perfil.objects.get_or_create(usuario=usuario, defaults={'tipo': tipo})