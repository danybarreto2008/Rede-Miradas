from django import forms
from .models import Perfil


class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = [
        'foto',
        'banner',
        'bio',
        'escola',
        'grupo',
        'logo_grupo',
        'nome_curta_participou',
        'foto_curta_participou',
        'link_curta_participou',
        'instagram',
        'link_outra_rede',
        'curtas_favoritos',
    ]

        widgets = {
            'curtas_favoritos': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        campos_texto = ['bio', 'escola', 'grupo', 'nome_curta_participou', 'link_curta_participou', 'instagram', 'link_outra_rede']

        for nome_campo in campos_texto:
            self.fields[nome_campo].widget.attrs.update({'class': 'form-control'})

        self.fields['bio'].widget.attrs.update({'rows': 4, 'placeholder': 'Conte um pouco sobre você...'})