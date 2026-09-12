from django.contrib import admin
from django import forms

from .models import (
    Destaque,
    Noticia,
    BlocoApresentacao,
    Curta,
    SecaoCurtas,
    SecaoFinal,
    TrilhasHero,
    TrilhasFaixaItem,
    TrilhasCard
)

class DestaqueForm(forms.ModelForm):

    class Meta:
        model = Destaque

        fields = '__all__'

        widgets = {

            'cor_titulo': forms.TextInput(
                attrs={
                    'type': 'color'
                }
            ),

            'cor_texto': forms.TextInput(
                attrs={
                    'type': 'color'
                }
            ),

            'cor_fundo_botao': forms.TextInput(
                attrs={
                    'type': 'color'
                }
            ),

            'cor_texto_botao': forms.TextInput(
                attrs={
                    'type': 'color'
                }
            ),

            'cor_borda_botao': forms.TextInput(
                attrs={
                    'type': 'color'
                }
            ),
        }
        
class BlocoApresentacaoForm(forms.ModelForm):

    class Meta:
        model = BlocoApresentacao

        fields = '__all__'

        widgets = {

            'cor_gradiente_1': forms.TextInput(
                attrs={
                    'type': 'color'
                }
            ),

            'cor_gradiente_2': forms.TextInput(
                attrs={
                    'type': 'color'
                }
            ),
        }


@admin.register(BlocoApresentacao)
class BlocoApresentacaoAdmin(admin.ModelAdmin):

    form = BlocoApresentacaoForm

    list_display = (
        'emoji',
        'texto',
        'ordem',
        'ativo',
    )

    list_editable = (
        'ordem',
        'ativo',
    )

    ordering = (
        'ordem',
    )
    
@admin.register(SecaoCurtas)
class SecaoCurtasAdmin(admin.ModelAdmin):

    list_display = (
        'titulo',
        'subtitulo',
    )

@admin.register(Destaque)
class DestaqueAdmin(admin.ModelAdmin):

    form = DestaqueForm

    list_display = (
        'titulo',
        'ordem',
        'ativo',
        'posicao_horizontal',
        'posicao_vertical',
    )

    list_editable = (
        'ordem',
        'ativo',
    )

    ordering = (
        'ordem',
    )

class CurtaForm(forms.ModelForm):

    class Meta:
        model = Curta

        fields = '__all__'

        widgets = {

            'cor_borda_1': forms.TextInput(
                attrs={
                    'type': 'color'
                }
            ),

            'cor_borda_2': forms.TextInput(
                attrs={
                    'type': 'color'
                }
            ),
        }


@admin.register(Curta)
class CurtaAdmin(admin.ModelAdmin):

    form = CurtaForm

    list_display = (
        'id',
        'link_youtube',
        'ordem',
        'ativo',
    )

    list_editable = (
        'ordem',
        'ativo',
    )

    ordering = (
        'ordem',
    )

@admin.register(SecaoFinal)
class SecaoFinalAdmin(admin.ModelAdmin):

    list_display = (
        'titulo',
    )

class NoticiaForm(forms.ModelForm):

    class Meta:
        model = Noticia
        fields = '__all__'
        widgets = {
            'cor_fundo_destaque': forms.TextInput(attrs={'type': 'color'}),
        }


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):

    form = NoticiaForm

    list_display = (
        'titulo',
        'categoria',
        'data_publicacao',
        'destaque',
        'publicada',
    )

    list_filter = (
        'categoria',
        'destaque',
        'publicada',
    )

    search_fields = (
        'titulo',
        'resumo',
        'texto',
    )

    prepopulated_fields = {
        'slug': ('titulo',)
    }

    ordering = (
        '-data_publicacao',
    )

    fieldsets = (
            ('Conteúdo', {
                'fields': ('titulo', 'slug', 'categoria', 'resumo', 'texto', 'imagem')
            }),
            ('Destaque', {
                'fields': ('destaque', 'destaque_secundario', 'cor_fundo_destaque'),
                'description': 'A cor de fundo é usada tanto no destaque principal quanto nos cards de destaque secundário.'
            }),
            ('Publicação', {
                'fields': ('publicada',)
            }),
    )

# Admin - Página Inicial das Trilhas de Aprendizagem

class TrilhasHeroForm(forms.ModelForm):

    class Meta:
        model = TrilhasHero
        fields = '__all__'
        widgets = {
            'cor_titulo': forms.TextInput(attrs={'type': 'color'}),
            'cor_subtitulo': forms.TextInput(attrs={'type': 'color'}),
            'cor_fundo_botao': forms.TextInput(attrs={'type': 'color'}),
            'cor_texto_botao': forms.TextInput(attrs={'type': 'color'}),
            'cor_glow_1': forms.TextInput(attrs={'type': 'color'}),
            'cor_glow_2': forms.TextInput(attrs={'type': 'color'}),
        }


@admin.register(TrilhasHero)
class TrilhasHeroAdmin(admin.ModelAdmin):
    form = TrilhasHeroForm
    list_display = (
        'titulo',
        'subtitulo',
        'texto_botao',
        'mostrar_botao',
    )


@admin.register(TrilhasFaixaItem)
class TrilhasFaixaItemAdmin(admin.ModelAdmin):
    list_display = (
        'texto',
        'ordem',
        'ativo',
    )
    list_editable = (
        'ordem',
        'ativo',
    )
    ordering = (
        'ordem',
    )


class TrilhasCardForm(forms.ModelForm):

    class Meta:
        model = TrilhasCard
        fields = '__all__'
        widgets = {
            'cor_fundo_card': forms.TextInput(attrs={'type': 'color'}),
            'cor_borda_card': forms.TextInput(attrs={'type': 'color'}),
            'cor_glow': forms.TextInput(attrs={'type': 'color'}),
            'cor_tag': forms.TextInput(attrs={'type': 'color'}),
            'cor_titulo': forms.TextInput(attrs={'type': 'color'}),
            'cor_descricao': forms.TextInput(attrs={'type': 'color'}),
            'cor_fundo_botao': forms.TextInput(attrs={'type': 'color'}),
            'cor_texto_botao': forms.TextInput(attrs={'type': 'color'}),
        }


@admin.register(TrilhasCard)
class TrilhasCardAdmin(admin.ModelAdmin):
    form = TrilhasCardForm
    list_display = (
        'tag',
        'titulo',
        'tipo_icone',
        'ordem',
        'ativo',
    )
    list_editable = (
        'ordem',
        'ativo',
    )
    ordering = (
        'ordem',
    )
