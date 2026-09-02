from django.contrib import admin
from django import forms

from .models import Destaque


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