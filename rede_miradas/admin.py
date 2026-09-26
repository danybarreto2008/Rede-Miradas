from django.contrib import admin
from django import forms
from django.db.models import Count
from .models import (
    Destaque,
    Noticia,
    BlocoApresentacao,
    Curta,
    SecaoCurtas,
    SecaoFinal,
    Perfil,
    TrilhasHero,
    TrilhasFaixaItem,
    TrilhasCard,
    SubtopicoTrilha,
    Voto,
    CurtaVotacao,
)
@admin.register(CurtaVotacao)
class CurtaVotacaoAdmin(admin.ModelAdmin):

    list_display = (
        'titulo',
        'grupo',
        'turma',
        'ordem',
        'ativo',
        'quantidade_votos',
    )

    list_editable = (
        'ordem',
        'ativo',
    )

    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        return queryset.annotate(
            quantidade_votos=Count('votos')
        ).order_by('-quantidade_votos')

    def quantidade_votos(self, obj):
        return obj.quantidade_votos

    quantidade_votos.short_description = 'Votos'
    quantidade_votos.admin_order_field = 'quantidade_votos'


@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):

    list_display = (
        'curta',
        'usuario',
        'data_voto',
    )

    list_filter = (
        'curta',
    )

    ordering = (
        '-data_voto',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):

    list_display = (
        'usuario',
        'tipo',
    )

    list_filter = (
        'tipo',
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

    list_display = (
        'nome',
        'grupo',
        'ativo',
        'ordem',
    )

    list_editable = (
        'ativo',
        'ordem',
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


class SubtopicoTrilhaInline(admin.TabularInline):
    model = SubtopicoTrilha
    extra = 1
    fields = ('ordem', 'titulo', 'link', 'mostrar_botao_comecar', 'ativo')


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
    inlines = [SubtopicoTrilhaInline]
    list_display = (
        'tag',
        'titulo',
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
    fieldsets = (
        ('Conteúdo da Trilha', {
            'fields': ('tag', 'titulo', 'descricao', 'imagem_capa')
        }),
        ('Botão de Ação', {
            'fields': ('mostrar_botao', 'texto_botao', 'link_botao')
        }),
        ('Personalização Visual (Cores)', {
            'fields': (
                'cor_fundo_card',
                'cor_borda_card',
                'estilo_borda',
                'cor_glow',
                'cor_tag',
                'cor_titulo',
                'cor_descricao',
                'cor_fundo_botao',
                'cor_texto_botao',
            ),
            'classes': ('collapse',),
        }),
        ('Formatação de Texto', {
            'fields': (
                'tag_negrito',
                'tag_italico',
                'titulo_negrito',
                'titulo_italico',
                'descricao_negrito',
                'descricao_italico',
            ),
            'classes': ('collapse',),
        }),
        ('Controle de Exibição', {
            'fields': ('ordem', 'ativo', 'tipo_icone', 'icone_personalizado')
        }),
    )


@admin.register(SubtopicoTrilha)
class SubtopicoTrilhaAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'trilha',
        'ordem',
        'ativo',
    )
    list_editable = (
        'ordem',
        'ativo',
    )
    list_filter = (
        'trilha',
        'ativo',
    )
    search_fields = (
        'titulo',
        'trilha__titulo',
    )
    ordering = (
        'trilha',
        'ordem',
    )

