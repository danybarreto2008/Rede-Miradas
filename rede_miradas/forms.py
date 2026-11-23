# ruff: noqa: RUF012
from django import forms
from django.forms import inlineformset_factory

from .models import Curta, Perfil, ProducaoPerfil

MAX_FAVORITOS = 4
MAX_PRODUCOES = 6


def _validar_youtube(link):
    """Aceita só links do YouTube (ou vazio)."""
    link = (link or "").strip()

    if link and not any(
        dominio in link.lower() for dominio in ["youtube.com", "youtu.be"]
    ):
        raise forms.ValidationError(
            "Por favor, insira um link válido do YouTube "
            "(ex: https://www.youtube.com/watch?v=... ou https://youtu.be/...)."
        )

    return link


def _montar_link_rede(valor, base):
    """
    Deixa o usuário digitar só o @ do perfil.
    "@maria"  -> https://base/maria
    "site.com/maria" -> https://site.com/maria
    """
    valor = (valor or "").strip()

    if not valor:
        return ""

    if valor.startswith(("http://", "https://")):
        return valor

    if "." in valor and "/" in valor:
        return f"https://{valor}"

    return f"https://{base}/{valor.lstrip('@')}"


class PerfilForm(forms.ModelForm):
    instagram = forms.CharField(
        required=False,
        max_length=200,
        help_text="Ex: @seuperfil ou https://instagram.com/seuperfil",
    )

    facebook = forms.CharField(required=False, max_length=200)

    vsco = forms.CharField(required=False, max_length=200)

    ocupacoes_escolhidas = forms.MultipleChoiceField(
        choices=Perfil.OCUPACOES_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Perfil
        fields = [
            "foto",
            "banner",
            "bio",
            "escola",
            "cidade",
            "data_nascimento",
            "facebook",
            "instagram",
            "vsco",
            "link_outra_rede",
            "curtas_favoritos",
        ]

        widgets = {
            "foto": forms.FileInput(attrs={"accept": "image/*"}),
            "banner": forms.FileInput(attrs={"accept": "image/*"}),
            "data_nascimento": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "curtas_favoritos": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # só curtas ativos podem ser favoritados
        self.fields["curtas_favoritos"].queryset = Curta.objects.filter(
            ativo=True
        )

        # marca as características já salvas
        if self.instance and self.instance.pk:
            self.fields["ocupacoes_escolhidas"].initial = [
                c for c in self.instance.ocupacoes.split(",") if c
            ]

        campos_texto = [
            "bio",
            "escola",
            "cidade",
            "data_nascimento",
            "facebook",
            "instagram",
            "vsco",
            "link_outra_rede",
        ]

        for nome_campo in campos_texto:
            self.fields[nome_campo].widget.attrs.update(
                {"class": "campo-input"}
            )

        self.fields["bio"].widget.attrs.update(
            {
                "rows": 5,
                "maxlength": 300,
                "placeholder": "Conte um pouco sobre você...",
            }
        )
        self.fields["escola"].widget.attrs["placeholder"] = (
            "Ex: IFRN - Campus Natal Central"
        )
        self.fields["cidade"].widget.attrs["placeholder"] = "Ex: Natal - RN"
        self.fields["facebook"].widget.attrs["placeholder"] = (
            "@seuperfil ou link"
        )
        self.fields["instagram"].widget.attrs["placeholder"] = (
            "@seuperfil ou link"
        )
        self.fields["vsco"].widget.attrs["placeholder"] = "@seuperfil ou link"
        self.fields["link_outra_rede"].widget.attrs["placeholder"] = (
            "https://..."
        )

    def clean_curtas_favoritos(self):
        curtas = self.cleaned_data.get("curtas_favoritos")

        if curtas is not None and len(curtas) > MAX_FAVORITOS:
            raise forms.ValidationError(
                f"Escolha no máximo {MAX_FAVORITOS} curtas favoritos."
            )

        return curtas

    def clean_instagram(self):
        return _montar_link_rede(
            self.cleaned_data.get("instagram"), "instagram.com"
        )

    def clean_facebook(self):
        return _montar_link_rede(
            self.cleaned_data.get("facebook"), "facebook.com"
        )

    def clean_vsco(self):
        return _montar_link_rede(self.cleaned_data.get("vsco"), "vsco.co")

    def save(self, commit=True):
        # junta as características escolhidas em um texto só
        self.instance.ocupacoes = ",".join(
            self.cleaned_data.get("ocupacoes_escolhidas", [])
        )
        return super().save(commit=commit)


class ProducaoPerfilForm(forms.ModelForm):
    class Meta:
        model = ProducaoPerfil
        fields = ["nome", "link_youtube", "cartaz"]

        widgets = {
            "cartaz": forms.FileInput(attrs={"accept": "image/*"}),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["nome"].widget.attrs.update(
            {"class": "campo-input", "placeholder": "Nome do curta"}
        )
        self.fields["link_youtube"].widget.attrs.update(
            {"class": "campo-input", "placeholder": "https://youtu.be/..."}
        )

    def clean_link_youtube(self):
        return _validar_youtube(self.cleaned_data.get("link_youtube"))


# lista de curtas que o usuário produziu (até 6)
ProducaoFormSet = inlineformset_factory(
    Perfil,
    ProducaoPerfil,
    form=ProducaoPerfilForm,
    extra=3,
    can_delete=True,
    max_num=MAX_PRODUCOES,
)