from django.db import models


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
        return f'Curta {self.id}'



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

    # Informações principais da notícia

    titulo = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True
    )

    categoria = models.CharField(
        max_length=30,
        choices=CATEGORIAS
    )

    resumo = models.TextField(
        max_length=300
    )

    texto = models.TextField()

    # Imagem da notícia

    imagem = models.ImageField(
        upload_to='noticias/'
    )

    # Data de publicação

    data_publicacao = models.DateTimeField(
        auto_now_add=True
    )

    # Controle da notícia

    destaque = models.BooleanField(
        default=False
    )

    publicada = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.titulo