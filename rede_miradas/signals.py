from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.dispatch import receiver
from .models import Perfil, conceder_selo


def _tipo_por_dados(dados):
    if not dados:
        return Perfil.ALUNO
    tipo_vinculo = dados.get('tipo_vinculo', '').lower()
    if 'servidor' in tipo_vinculo or 'professor' in tipo_vinculo or 'docente' in tipo_vinculo:
        return Perfil.PROFESSOR
    return Perfil.ALUNO


@receiver(user_signed_up)
def criar_perfil_ao_cadastrar(sender, request, user, **kwargs):
    sociallogin = kwargs.get('sociallogin')
    if sociallogin and sociallogin.account.provider == 'suap':
        dados = sociallogin.account.extra_data
        tipo = _tipo_por_dados(dados)
    else:
        tipo = Perfil.COMUM

    perfil, _ = Perfil.objects.get_or_create(usuario=user, defaults={'tipo': tipo})
    if sociallogin and sociallogin.account.provider == 'suap':
        perfil.tipo = tipo
        perfil.save()

    conceder_selo(user, 'primeiro-login')


@receiver(pre_social_login)
def criar_ou_atualizar_perfil_ao_logar_social(sender, request, sociallogin, **kwargs):
    usuario = sociallogin.user
    if not usuario or not usuario.pk:
        return

    dados = sociallogin.account.extra_data
    if sociallogin.account.provider == 'suap':
        tipo = _tipo_por_dados(dados)
        perfil, criado = Perfil.objects.get_or_create(usuario=usuario, defaults={'tipo': tipo})
        if not criado and perfil.tipo != tipo:
            perfil.tipo = tipo
            perfil.save()
    else:
        perfil, _ = Perfil.objects.get_or_create(usuario=usuario, defaults={'tipo': Perfil.COMUM})

    conceder_selo(usuario, 'primeiro-login')


@receiver(social_account_added)
def associar_perfil_ao_conectar_social(sender, request, sociallogin, **kwargs):
    usuario = sociallogin.user
    if not usuario or not usuario.pk:
        return

    dados = sociallogin.account.extra_data
    if sociallogin.account.provider == 'suap':
        tipo = _tipo_por_dados(dados)
        perfil, _ = Perfil.objects.get_or_create(usuario=usuario, defaults={'tipo': tipo})
        perfil.tipo = tipo
        perfil.save()

    conceder_selo(usuario, 'primeiro-login')