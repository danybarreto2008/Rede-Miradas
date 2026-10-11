# ruff: noqa: RUF012
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import (
    BlocoApresentacao,
    Curta,
    CurtaVotacao,
    Destaque,
    Noticia,
    Perfil,
    SecaoCurtas,
    SecaoFinal,
    SubtopicoTrilha,
    TopicoUnidadeTrilha,
    TrilhasCard,
    TrilhasFaixaItem,
    TrilhasHero,
    UnidadeTrilha,
)


class DestaqueForm(forms.ModelForm):
    class Meta:
        model = Destaque
        fields = [
            "titulo",
            "texto",
            "imagem",
            "cor_titulo",
            "cor_texto",
            "titulo_negrito",
            "titulo_italico",
            "titulo_sublinhado",
            "texto_negrito",
            "texto_italico",
            "texto_sublinhado",
            "mostrar_botao",
            "texto_botao",
            "link_botao",
            "cor_fundo_botao",
            "cor_texto_botao",
            "botao_com_borda",
            "cor_borda_botao",
            "botao_negrito",
            "botao_italico",
            "botao_sublinhado",
            "posicao_horizontal",
            "posicao_vertical",
            "ordem",
            "ativo",
        ]
        widgets = {
            "cor_titulo": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_texto": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_fundo_botao": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_texto_botao": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_borda_botao": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título do destaque na Tela Inicial",
                }
            ),
            "texto": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Descrição ou texto do destaque",
                }
            ),
            "imagem": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "texto_botao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Saiba mais",
                }
            ),
            "link_botao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: /trilhas/ ou https://...",
                }
            ),
            "posicao_horizontal": forms.Select(attrs={"class": "form-select"}),
            "posicao_vertical": forms.Select(attrs={"class": "form-select"}),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "mostrar_botao": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "botao_com_borda": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "titulo_negrito": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "titulo_italico": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "titulo_sublinhado": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "texto_negrito": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "texto_italico": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "texto_sublinhado": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "botao_negrito": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "botao_italico": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "botao_sublinhado": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class BlocoApresentacaoForm(forms.ModelForm):
    class Meta:
        model = BlocoApresentacao
        fields = [
            "emoji",
            "texto",
            "cor_gradiente_1",
            "cor_gradiente_2",
            "ordem",
            "ativo",
        ]
        widgets = {
            "emoji": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex: 🎬 ou 🚀"}
            ),
            "texto": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Texto explicativo do card",
                }
            ),
            "cor_gradiente_1": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_gradiente_2": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SecaoCurtasForm(forms.ModelForm):
    class Meta:
        model = SecaoCurtas
        fields = ["titulo", "subtitulo"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "CURTAS EM DESTAQUE",
                }
            ),
            "subtitulo": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Subtítulo da seção",
                }
            ),
        }


class CurtaForm(forms.ModelForm):
    class Meta:
        model = Curta
        fields = [
            "nome",
            "grupo",
            "cartaz",
            "link_youtube",
            "cor_borda_1",
            "cor_borda_2",
            "ordem",
            "ativo",
        ]
        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título da produção audiovisual",
                }
            ),
            "grupo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome da equipe ou grupo produtor",
                }
            ),
            "cartaz": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "link_youtube": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://www.youtube.com/watch?v=...",
                }
            ),
            "cor_borda_1": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_borda_2": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SecaoFinalForm(forms.ModelForm):
    class Meta:
        model = SecaoFinal
        fields = ["titulo", "subtitulo", "texto_botao", "link_botao"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "PRONTO PARA DAR VIDA ÀS SUAS IDEIAS?",
                }
            ),
            "subtitulo": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Texto da chamada final",
                }
            ),
            "texto_botao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Comece Agora",
                }
            ),
            "link_botao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: /trilhas/ ou https://...",
                }
            ),
        }


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = [
            "titulo",
            "slug",
            "categoria",
            "resumo",
            "texto",
            "imagem",
            "destaque",
            "destaque_secundario",
            "cor_fundo_destaque",
            "publicada",
        ]
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título da matéria ou notícia",
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "slug-amigavel-para-url",
                }
            ),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "resumo": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Resumo breve",
                }
            ),
            "texto": CKEditor5Widget(config_name="default"),
            "imagem": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "cor_fundo_destaque": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "destaque": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "destaque_secundario": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "publicada": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }


class TrilhasHeroForm(forms.ModelForm):
    class Meta:
        model = TrilhasHero
        fields = [
            "titulo",
            "subtitulo",
            "imagem_fundo",
            "mostrar_botao",
            "texto_botao",
            "link_botao",
            "cor_titulo",
            "cor_subtitulo",
            "cor_fundo_botao",
            "cor_texto_botao",
            "cor_glow_1",
            "cor_glow_2",
            "titulo_negrito",
            "titulo_italico",
            "subtitulo_negrito",
            "subtitulo_italico",
        ]
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Bem-Vindo(a)",
                }
            ),
            "subtitulo": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "imagem_fundo": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "mostrar_botao": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "texto_botao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Conheça as trilhas",
                }
            ),
            "link_botao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "/trilhas/visao-geral/",
                }
            ),
            "cor_titulo": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_subtitulo": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_fundo_botao": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_texto_botao": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_glow_1": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_glow_2": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "titulo_negrito": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "titulo_italico": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "subtitulo_negrito": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "subtitulo_italico": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }


class TrilhasFaixaItemForm(forms.ModelForm):
    class Meta:
        model = TrilhasFaixaItem
        fields = ["texto", "ordem", "ativo"]
        widgets = {
            "texto": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex: 5 ETAPAS"}
            ),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class TrilhasCardForm(forms.ModelForm):
    class Meta:
        model = TrilhasCard
        fields = [
            "tag",
            "slug",
            "titulo",
            "titulo_detalhe",
            "descricao",
            "imagem_capa",
            "tipo_icone",
            "icone_personalizado",
            "mostrar_botao",
            "texto_botao",
            "link_botao",
            "cor_fundo_card",
            "cor_borda_card",
            "estilo_borda",
            "cor_glow",
            "cor_tag",
            "cor_titulo",
            "cor_descricao",
            "cor_fundo_botao",
            "cor_texto_botao",
            "cor_sidebar",
            "cor_sidebar_topo",
            "tag_negrito",
            "tag_italico",
            "titulo_negrito",
            "titulo_italico",
            "descricao_negrito",
            "descricao_italico",
            "ordem",
            "ativo",
        ]
        widgets = {
            "tag": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Etapa 1 ou INSCRIÇÃO DAS EQUIPES",
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "inscricao-das-equipes",
                }
            ),
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título da Trilha",
                }
            ),
            "titulo_detalhe": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título detalhado na página de conteúdo",
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Descrição dos módulos",
                }
            ),
            "imagem_capa": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "tipo_icone": forms.Select(attrs={"class": "form-select"}),
            "icone_personalizado": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "mostrar_botao": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "texto_botao": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Começar"}
            ),
            "link_botao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "/trilhas/visao-geral/",
                }
            ),
            "estilo_borda": forms.Select(attrs={"class": "form-select"}),
            "cor_fundo_card": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_borda_card": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_glow": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_tag": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_titulo": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_descricao": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_fundo_botao": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_texto_botao": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_sidebar": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "cor_sidebar_topo": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            ),
            "tag_negrito": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "tag_italico": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "titulo_negrito": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "titulo_italico": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "descricao_negrito": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "descricao_italico": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class UnidadeTrilhaForm(forms.ModelForm):
    class Meta:
        model = UnidadeTrilha
        fields = ["trilha", "numero", "titulo", "ordem", "ativo"]
        widgets = {
            "trilha": forms.Select(attrs={"class": "form-select"}),
            "numero": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome da unidade (ex: Identidade Visual)",
                }
            ),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class TopicoUnidadeTrilhaForm(forms.ModelForm):
    class Meta:
        model = TopicoUnidadeTrilha
        fields = ["unidade", "titulo", "conteudo", "ordem", "ativo"]
        widgets = {
            "unidade": forms.Select(attrs={"class": "form-select"}),
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título da aula ou tópico",
                }
            ),
            "conteudo": CKEditor5Widget(config_name="default"),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SubtopicoTrilhaForm(forms.ModelForm):
    class Meta:
        model = SubtopicoTrilha
        fields = [
            "trilha",
            "titulo",
            "link",
            "mostrar_botao_comecar",
            "ordem",
            "ativo",
        ]
        widgets = {
            "trilha": forms.Select(attrs={"class": "form-select"}),
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título do item",
                }
            ),
            "link": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Link (opcional)",
                }
            ),
            "mostrar_botao_comecar": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CurtaVotacaoForm(forms.ModelForm):
    class Meta:
        model = CurtaVotacao
        fields = ["titulo", "grupo", "turma", "cartaz", "ordem", "ativo"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome do curta"}
            ),
            "grupo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome do grupo"}
            ),
            "turma": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Turma"}
            ),
            "cartaz": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class PerfilAdminForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            "tipo",
            "bio",
            "escola",
            "grupo",
            "nome_curta_participou",
            "link_curta_participou",
            "instagram",
            "link_outra_rede",
        ]
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "escola": forms.TextInput(attrs={"class": "form-control"}),
            "grupo": forms.TextInput(attrs={"class": "form-control"}),
            "nome_curta_participou": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "link_curta_participou": forms.URLInput(
                attrs={"class": "form-control"}
            ),
            "instagram": forms.URLInput(attrs={"class": "form-control"}),
            "link_outra_rede": forms.URLInput(attrs={"class": "form-control"}),
        }
