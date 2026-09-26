from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User


# Curta que participa da votação do júri popular
class CurtaVotacao(models.Model):

    cartaz = models.ImageField(
        upload_to='votacao/'
    )

    titulo = models.CharField(
        max_length=200
    )

    grupo = models.CharField(
        max_length=150,
        verbose_name='Nome do grupo'
    )

    turma = models.CharField(
        max_length=100
    )

    ativo = models.BooleanField(
        default=True
    )

    ordem = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        verbose_name = 'Curta em votação'
        verbose_name_plural = 'Curtas em votação'
        ordering = ['ordem']

    def __str__(self):
        return self.titulo


# Voto de um usuário — só pode ter UM voto no total (OneToOneField garante isso)
class Voto(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    curta = models.ForeignKey(
        CurtaVotacao,
        on_delete=models.CASCADE,
        related_name='votos'
    )

    data_voto = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'

    def __str__(self):
        return f'{self.usuario} → {self.curta}'
    
# Diz se o usuário é Aluno ou Professor, ou comum
class Perfil(models.Model):

    ALUNO = 'aluno'
    PROFESSOR = 'professor'
    COMUM = 'comum'

    TIPO_CHOICES = [
        (ALUNO, 'Aluno'),
        (PROFESSOR, 'Professor'),
        (COMUM, 'Usuário comum'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES
    )

    foto = models.ImageField(
        upload_to='perfis/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        max_length=300,
        blank=True
    )

    escola = models.CharField(
        max_length=150,
        blank=True
    )

    grupo = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Grupo/equipe'
    )

    nome_curta_participou = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Curta que participei'
    )

    logo_grupo = models.ImageField(
    upload_to='logos_grupos/',
    blank=True,
    null=True
    )

    foto_curta_participou = models.ImageField(
        upload_to='curtas_usuarios/',
        blank=True,
        null=True
    )

    banner = models.ImageField(
    upload_to='banners_perfil/',
    blank=True,
    null=True
    )

    link_curta_participou = models.URLField(
        blank=True,
        verbose_name='Link do YouTube do meu curta'
    )

    instagram = models.URLField(
        blank=True
    )

    link_outra_rede = models.URLField(
        blank=True,
        verbose_name='Outra rede social / portfólio'
    )

    curtas_favoritos = models.ManyToManyField(
        'Curta',
        blank=True,
        related_name='favoritado_por'
    )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'{self.usuario} ({self.get_tipo_display()})'
    
# Modelo dos destaques da página "Comece por aqui"
class Destaque(models.Model):

    POSICAO_HORIZONTAL = [
        ('esquerda', 'Esquerda'),
        ('centro', 'Centro'),
        ('direita', 'Direita'),
    ]

    POSICAO_VERTICAL = [
        ('topo', 'Topo'),
        ('meio', 'Meio'),
        ('baixo', 'Baixo'),
    ]

    # Conteúdo

    titulo = models.CharField(
        max_length=200,
        blank=True
    )

    texto = models.TextField(
        blank=True
    )

    imagem = models.ImageField(
        upload_to='destaques/'
    )

    # Cores do título e do texto

    cor_titulo = models.CharField(
        max_length=7,
        default='#FFFFFF'
    )

    cor_texto = models.CharField(
        max_length=7,
        default='#FFFFFF'
    )

    # Formatação do título e do texto

    titulo_negrito = models.BooleanField(
        default=False
    )

    titulo_italico = models.BooleanField(
        default=False
    )

    titulo_sublinhado = models.BooleanField(
        default=False
    )

    texto_negrito = models.BooleanField(
        default=False
    )

    texto_italico = models.BooleanField(
        default=False
    )

    texto_sublinhado = models.BooleanField(
        default=False
    )

    # Botão

    mostrar_botao = models.BooleanField(
        default=True
    )

    texto_botao = models.CharField(
        max_length=100,
        blank=True
    )

    link_botao = models.URLField(
        blank=True
    )

    # Cor do fundo do botão

    cor_fundo_botao = models.CharField(
        max_length=7,
        default='#FFFFFF'
    )

    # Cor do texto do botão

    cor_texto_botao = models.CharField(
        max_length=7,
        default='#000000'
    )

    # Borda do botão

    botao_com_borda = models.BooleanField(
        default=False
    )

    cor_borda_botao = models.CharField(
        max_length=7,
        default='#FFFFFF'
    )

    # Formatação do botão

    botao_negrito = models.BooleanField(
        default=True
    )

    botao_italico = models.BooleanField(
        default=False
    )

    botao_sublinhado = models.BooleanField(
        default=False
    )

    # Posição do conteúdo

    posicao_horizontal = models.CharField(
        max_length=20,
        choices=POSICAO_HORIZONTAL,
        default='esquerda'
    )

    posicao_vertical = models.CharField(
        max_length=20,
        choices=POSICAO_VERTICAL,
        default='meio'
    )

    # Controle do destaque

    ativo = models.BooleanField(
        default=True
    )

    ordem = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.titulo or f'Destaque {self.id}'

# Modelo dos cards "Aprenda. Crie. Conecte." da página "Comece por aqui"
class BlocoApresentacao(models.Model):

    # Conteúdo

    emoji = models.CharField(
        max_length=10,
        help_text='Emoji exibido no topo do card. Ex: 🎬'
    )

    texto = models.TextField(
        max_length=200
    )

    # Degradê da borda

    cor_gradiente_1 = models.CharField(
        max_length=7,
        default='#8b2ff7'
    )

    cor_gradiente_2 = models.CharField(
        max_length=7,
        default='#22d3ee'
    )

    # Controle do card

    ativo = models.BooleanField(
        default=True
    )

    ordem = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        verbose_name = 'Bloco de apresentação'
        verbose_name_plural = 'Blocos de apresentação'

    def __str__(self):
        return self.texto[:40] if self.texto else f'Bloco {self.id}'
    
# Modelo do texto da seção "Curtas em destaque"
class SecaoCurtas(models.Model):

    titulo = models.CharField(
        max_length=200,
        default='CURTAS EM DESTAQUE'
    )

    subtitulo = models.CharField(
        max_length=300,
        blank=True
    )

    class Meta:
        verbose_name = 'Texto da seção de curtas'
        verbose_name_plural = 'Texto da seção de curtas'

    def __str__(self):
        return self.titulo
    # Modelo dos curtas em destaque da página "Comece por aqui"

class Curta(models.Model):

    nome = models.CharField(
        max_length=200,
        default='Sem nome'
    )

    grupo = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Nome do grupo'
    )

    cartaz = models.ImageField(
        upload_to='curtas/'
    )

    link_youtube = models.URLField()

    cor_borda_1 = models.CharField(
        max_length=7,
        default='#7C3AED'
    )

    cor_borda_2 = models.CharField(
        max_length=7,
        default='#06B6D4'
    )

    ativo = models.BooleanField(
        default=True
    )

    ordem = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        verbose_name = 'Curta em destaque'
        verbose_name_plural = 'Curtas em destaque'
        ordering = ['ordem']

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Curta em destaque'
        verbose_name_plural = 'Curtas em destaque'
        ordering = ['ordem']

    def __str__(self):
        return self.nome
# Modelo do texto da seção final (chamada para ação)
class SecaoFinal(models.Model):

    titulo = models.CharField(
        max_length=200,
        default='PRONTO PARA DAR VIDA ÀS SUAS IDEIAS?'
    )

    subtitulo = models.TextField(
        blank=True
    )

    texto_botao = models.CharField(
        max_length=50,
        blank=True
    )

    link_botao = models.URLField(
        blank=True
    )

    class Meta:
        verbose_name = 'Texto da seção final'
        verbose_name_plural = 'Texto da seção final'

    def __str__(self):
        return self.titulo
    
    
# Modelo das notícias do blog
class Noticia(models.Model):

    CATEGORIAS = [
        ('resultado', 'Resultado'),
        ('evento', 'Evento'),
        ('projeto', 'Projeto'),
        ('novidade', 'Novidade'),
        ('outros', 'Outros'),
    ]

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS)
    resumo = models.TextField(max_length=300)
    texto = CKEditor5Field('Texto', config_name='default')
    imagem = models.ImageField(upload_to='noticias/')
    data_publicacao = models.DateTimeField(auto_now_add=True)

    destaque = models.BooleanField(default=False)
    destaque_secundario = models.BooleanField(
        default=False,
        help_text='Aparece na seção de destaques abaixo dos posts recentes. Não entra mais na lista de "Últimas notícias".'
    )

    publicada = models.BooleanField(default=True)

    # Cor de fundo usada quando a notícia está marcada como destaque
    cor_fundo_destaque = models.CharField(
    max_length=7,
    default='#3A1660',
    help_text='Cor de fundo exibida na seção de destaque (só é usada quando "destaque" estiver marcado).'
    )

    def __str__(self):
        return self.titulo
    

# Modelos da Página Inicial das Trilhas de Aprendizagem

class TrilhasHero(models.Model):

    # Textos
    titulo = models.CharField(
        max_length=200,
        default='Bem-Vindo(a)',
        blank=True
    )

    subtitulo = models.TextField(
        default='Aprenda produção audiovisual em módulos práticos e criativos.',
        blank=True
    )

    imagem_fundo = models.ImageField(
        upload_to='trilhas/hero/',
        blank=True,
        null=True,
        help_text='Opcional. Se não enviada, mantém o fundo escuro com iluminação neon.'
    )

    # Botão
    mostrar_botao = models.BooleanField(
        default=True
    )

    texto_botao = models.CharField(
        max_length=100,
        default='Conheça as trilhas',
        blank=True
    )

    link_botao = models.CharField(
        max_length=255,
        default='/trilhas/visao-geral/',
        blank=True
    )

    # Cores
    cor_titulo = models.CharField(
        max_length=7,
        default='#FFFFFF'
    )

    cor_subtitulo = models.CharField(
        max_length=7,
        default='#FFFFFF'
    )

    cor_fundo_botao = models.CharField(
        max_length=7,
        default='#FFFFFF'
    )

    cor_texto_botao = models.CharField(
        max_length=7,
        default='#0B0C10'
    )

    cor_glow_1 = models.CharField(
        max_length=7,
        default='#7C3AED',
        help_text='Cor primária do brilho neon central'
    )

    cor_glow_2 = models.CharField(
        max_length=7,
        default='#22D3EE',
        help_text='Cor secundária do brilho neon central'
    )

    # Formatação
    titulo_negrito = models.BooleanField(
        default=True
    )

    titulo_italico = models.BooleanField(
        default=False
    )

    subtitulo_negrito = models.BooleanField(
        default=False
    )

    subtitulo_italico = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = 'Trilhas - Seção de Boas-Vindas (Hero)'
        verbose_name_plural = 'Trilhas - Seção de Boas-Vindas (Hero)'

    def __str__(self):
        return self.titulo or 'Seção de Boas-Vindas'


class TrilhasFaixaItem(models.Model):

    texto = models.CharField(
        max_length=100,
        help_text='Ex: 5 ETAPAS, DEZENAS DE MATERIAIS, EXERCÍCIOS, EXEMPLOS REAIS'
    )

    ordem = models.PositiveIntegerField(
        default=0
    )

    ativo = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'Trilhas - Item da Faixa Informativa'
        verbose_name_plural = 'Trilhas - Itens da Faixa Informativa'
        ordering = ['ordem']

    def __str__(self):
        return self.texto


class TrilhasCard(models.Model):

    CHOICES_ICONE = [
        ('equipes', 'Aperto de mão (Equipes)'),
        ('texto', 'Livro aberto (Texto Autoral)'),
        ('roteiro', 'Lápis (Roteiro)'),
        ('producao', 'Câmera de Cinema (Produção e Gravação)'),
        ('edicao', 'Ilha de Edição e Corte (Edição e Finalização)'),
        ('personalizado', 'Imagem / SVG personalizado'),
    ]

    CHOICES_BORDA = [
        ('dashed', 'Tracejada'),
        ('solid', 'Sólida'),
        ('dotted', 'Pontilhada'),
        ('none', 'Sem borda'),
    ]

    # Conteúdo
    tag = models.CharField(
        max_length=100,
        help_text='Ex: INSCRIÇÃO DAS EQUIPES'
    )

    titulo = models.CharField(
        max_length=250,
        help_text='Ex: Toda grande produção começa com uma boa equipe.'
    )

    descricao = models.TextField(
        help_text='Ex: Conheça a ficha de inscrição, apresente sua equipe...'
    )

    # Imagem de capa do Card (estilo Substack / Figma)
    imagem_capa = models.ImageField(
        upload_to='trilhas/capas/',
        blank=True,
        null=True,
        help_text='Imagem de capa ilustrativa do card da trilha'
    )

    # Ícone
    tipo_icone = models.CharField(
        max_length=30,
        choices=CHOICES_ICONE,
        default='equipes',
        help_text='Selecione o ícone ilustrado padrão ou envie uma imagem própria'
    )

    icone_personalizado = models.ImageField(
        upload_to='trilhas/icones/',
        blank=True,
        null=True,
        help_text='Opcional. Imagem ou SVG caso tenha selecionado ícone personalizado'
    )

    # Botão
    mostrar_botao = models.BooleanField(
        default=True
    )

    texto_botao = models.CharField(
        max_length=100,
        default='Começar',
        blank=True
    )

    link_botao = models.CharField(
        max_length=255,
        default='/trilhas/visao-geral/',
        blank=True
    )

    # Cores
    cor_fundo_card = models.CharField(
        max_length=7,
        default='#101535',
        help_text='Cor de fundo do card'
    )

    cor_borda_card = models.CharField(
        max_length=7,
        default='#1E2659',
        help_text='Cor da borda do card'
    )

    estilo_borda = models.CharField(
        max_length=20,
        choices=CHOICES_BORDA,
        default='solid'
    )

    cor_glow = models.CharField(
        max_length=7,
        default='#7C3AED',
        help_text='Cor do brilho neon no fundo do card'
    )

    cor_tag = models.CharField(
        max_length=7,
        default='#94A3B8',
        help_text='Cor da tag superior'
    )

    cor_titulo = models.CharField(
        max_length=7,
        default='#FFFFFF',
        help_text='Cor do título'
    )

    cor_descricao = models.CharField(
        max_length=7,
        default='#CBD5E1',
        help_text='Cor da descrição'
    )

    cor_fundo_botao = models.CharField(
        max_length=7,
        default='#B94B61',
        help_text='Cor de fundo do botão'
    )

    cor_texto_botao = models.CharField(
        max_length=7,
        default='#FFFFFF',
        help_text='Cor do texto do botão'
    )

    # Formatação de fontes
    tag_negrito = models.BooleanField(
        default=True
    )

    tag_italico = models.BooleanField(
        default=False
    )

    titulo_negrito = models.BooleanField(
        default=True
    )

    titulo_italico = models.BooleanField(
        default=False
    )

    descricao_negrito = models.BooleanField(
        default=False
    )

    descricao_italico = models.BooleanField(
        default=False
    )

    # Controle
    ativo = models.BooleanField(
        default=True
    )

    ordem = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        verbose_name = 'Trilhas - Card de Trilha'
        verbose_name_plural = 'Trilhas - Cards de Trilhas'
        ordering = ['ordem']

    def __str__(self):
        return f'{self.tag} - {self.titulo[:30]}'


class SubtopicoTrilha(models.Model):

    trilha = models.ForeignKey(
        TrilhasCard,
        on_delete=models.CASCADE,
        related_name='subtopicos'
    )

    titulo = models.CharField(
        max_length=255,
        help_text='Título do item/subtópico. Ex: CONTO e CRÔNICA: como diferenciar?'
    )

    link = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text='Link específico para o material ou aula (opcional). Se vazio, usará o link da trilha.'
    )

    mostrar_botao_comecar = models.BooleanField(
        default=False,
        help_text='Exibir o botão "Começar" ao lado deste item'
    )

    ordem = models.PositiveIntegerField(
        default=0
    )

    ativo = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'Subtópico da Trilha'
        verbose_name_plural = 'Subtópicos da Trilha'
        ordering = ['ordem']

    def __str__(self):
        return f'{self.trilha.titulo} - {self.titulo}'

