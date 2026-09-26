from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from .models import Perfil


def _tipo_por_dados(dados):
    tipo_vinculo = dados.get('tipo_vinculo', '').lower()
    if 'servidor' in tipo_vinculo or 'professor' in tipo_vinculo or 'docente' in tipo_vinculo:
        return Perfil.PROFESSOR
    return Perfil.ALUNO


@receiver(pre_social_login)
def criar_perfil_ao_logar_suap(sender, request, sociallogin, **kwargs):
    # rede de segurança: contas antigas que por algum motivo ficaram sem perfil
    if not sociallogin.is_existing:
        return
    usuario = sociallogin.user
    if hasattr(usuario, 'perfil'):
        return
    dados = sociallogin.account.extra_data
    Perfil.objects.get_or_create(usuario=usuario, defaults={'tipo': _tipo_por_dados(dados)})


@receiver(user_signed_up)
def criar_perfil_ao_cadastrar(sender, request, user, **kwargs):
    # cadastro novo via Google/SUAP: cria o perfil na hora
    sociallogin = kwargs.get('sociallogin')
    if not sociallogin:
        return
    if hasattr(user, 'perfil'):
        return
    dados = sociallogin.account.extra_data
    Perfil.objects.get_or_create(usuario=user, defaults={'tipo': _tipo_por_dados(dados)})