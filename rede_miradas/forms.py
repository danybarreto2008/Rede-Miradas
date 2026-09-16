from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CodigoProfessor


# Formulário de cadastro (usado por Aluno e Professor)
class CadastroForm(UserCreationForm):

    nome = forms.CharField(
        required=True,
        label='Nome completo',
        max_length=150
    )

    email = forms.EmailField(
        required=True,
        label='E-mail'
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            campo.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe uma conta com esse e-mail.')

        return email

    def save(self, commit=True):

        usuario = super().save(commit=False)

        usuario.username = self.cleaned_data['email']
        usuario.email = self.cleaned_data['email']
        usuario.first_name = self.cleaned_data['nome']

        if commit:
            usuario.save()

        return usuario


# Formulário de login (usado por Aluno e Professor)
class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'E-mail'

        for campo in self.fields.values():
            campo.widget.attrs.update({'class': 'form-control'})

# Formulário de cadastro do professor (exige código de acesso)
class CadastroProfessorForm(CadastroForm):

    codigo_acesso = forms.CharField(
        required=True,
        label='Código de acesso fornecido pela coordenação'
    )

    def clean_codigo_acesso(self):

        codigo_digitado = self.cleaned_data.get('codigo_acesso')

        codigo_valido = CodigoProfessor.objects.first()

        if not codigo_valido or codigo_digitado != codigo_valido.codigo:
            raise forms.ValidationError('Código de acesso inválido.')

        return codigo_digitado