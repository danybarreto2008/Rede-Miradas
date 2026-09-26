from django.apps import AppConfig


class RedeMiradasConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rede_miradas'

    def ready(self):
        import rede_miradas.signals