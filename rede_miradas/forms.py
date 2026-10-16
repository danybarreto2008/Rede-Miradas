# ruff: noqa: RUF012
from django import forms

from .models import Perfil


class PerfilForm(forms.ModelForm):
    instagram = forms.CharField(
        required=False,
        max_length=200,
        help_text="Ex: @seuperfil ou https://instagram.com/seuperfil",
    )

    class Meta:
        model = Perfil
        fields = [
            "foto",
            "banner",
            "bio",
            "escola",
            "grupo",
            "logo_grupo",
            "nome_curta_participou",
            "foto_curta_participou",
            "link_curta_participou",
            "instagram",
            "link_outra_rede",
            "curtas_favoritos",
        ]

        widgets = {
            "curtas_favoritos": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        campos_texto = [
            "bio",
            "escola",
            "grupo",
            "nome_curta_participou",
            "link_curta_participou",
            "instagram",
            "link_outra_rede",
        ]

        for nome_campo in campos_texto:
            self.fields[nome_campo].widget.attrs.update(
                {"class": "form-control"}
            )

        self.fields["bio"].widget.attrs.update(
            {"rows": 4, "placeholder": "Conte um pouco sobre você..."}
        )

    def clean_link_curta_participou(self):
        link = self.cleaned_data.get("link_curta_participou")
        if link:
            link = link.strip()
            if not any(
                dominio in link.lower() for dominio in ["youtube.com", "youtu.be"]
            ):
                raise forms.ValidationError(
                    "Por favor, insira um link válido do YouTube (ex: https://www.youtube.com/watch?v=... ou https://youtu.be/...)."
                )
        return link

    def clean_instagram(self):
        val = self.cleaned_data.get("instagram", "").strip()
        if not val:
            return ""
        if val.startswith(("http://", "https://")):
            return val
        val = val.lstrip("@")
        return f"https://instagram.com/{val}"
