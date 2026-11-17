# ruff: noqa: RUF012
from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# Registro de quem ganhou qual selo e quando
# (o conteúdo do selo fica em selos.py)
class SeloConquistado(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="selos_conquistados"
    )

    selo = models.SlugField(
        max_length=50,
        help_text="Identificador do selo, definido em rede_miradas/selos.py",
    )

    data_conquista = models.DateTimeField(auto_now_add=True)

    visualizado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Selo conquistado"
        verbose_name_plural = "Selos conquistados"
        unique_together = ("usuario", "selo")
        ordering = ["-data_conquista"]

    def __str__(self):
        return f"{self.usuario} → {self.selo}"


def conceder_selo(usuario, slug):
    """
    Concede um selo (pelo slug definido em selos.py) ao usuário, se ele
    ainda não tiver. Sua amiga usa a mesma função pro selo de trilha:
    conceder_selo(request.user, 'trilha-concluida')
    """
    conquista, criado = SeloConquistado.objects.get_or_create(
        usuario=usuario, selo=slug
    )
    return conquista if criado else None


# Curta que participa da votação do júri popular
class CurtaVotacao(models.Model):
    cartaz = models.ImageField(upload_to="votacao/")

    titulo = models.CharField(max_length=200)

    grupo = models.CharField(max_length=150, verbose_name="Nome do grupo")

    turma = models.CharField(max_length=100)

    ativo = models.BooleanField(default=True)

    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Curta em votação"
        verbose_name_plural = "Curtas em votação"
        ordering = ["ordem"]
        permissions = [
            ("pode_gerenciar_votacao", "Pode gerenciar curtas em votação"),
        ]

    def __str__(self):
        return str(self.titulo)


# Voto de um usuário — só pode ter UM voto no total
# (OneToOneField garante isso)
class Voto(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    # E-mail usado na votação (sempre minúsculo). Único: 1 voto por e-mail.
    email = models.EmailField(
        "E-mail do votante",
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )

    curta = models.ForeignKey(
        CurtaVotacao, on_delete=models.CASCADE, related_name="votos"
    )
    # ... o resto continua igual

    data_voto = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Voto"
        verbose_name_plural = "Votos"
        ordering = ["-data_voto"]

    def __str__(self):
        return f"{self.usuario} → {self.curta}"


# Diz se o usuário é Aluno ou Professor, ou comum
class Perfil(models.Model):
    ALUNO = "aluno"
    PROFESSOR = "professor"
    COMUM = "comum"

    TIPO_CHOICES = [
        (ALUNO, "Aluno"),
        (PROFESSOR, "Professor"),
        (COMUM, "Usuário comum"),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    foto = models.ImageField(upload_to="perfis/", blank=True, null=True)

    bio = models.TextField(max_length=300, blank=True)

    escola = models.CharField(max_length=150, blank=True)

    grupo = models.CharField(
        max_length=150, blank=True, verbose_name="Grupo/equipe"
    )

    nome_curta_participou = models.CharField(
        max_length=200, blank=True, verbose_name="Curta que participei"
    )

    logo_grupo = models.ImageField(
        upload_to="logos_grupos/", blank=True, null=True
    )

    foto_curta_participou = models.ImageField(
        upload_to="curtas_usuarios/", blank=True, null=True
    )

    banner = models.ImageField(
        upload_to="banners_perfil/", blank=True, null=True
    )

    link_curta_participou = models.URLField(
        blank=True, verbose_name="Link do YouTube do meu curta"
    )

    instagram = models.URLField(blank=True)

    link_outra_rede = models.URLField(
        blank=True, verbose_name="Outra rede social / portfólio"
    )

    curtas_favoritos = models.ManyToManyField(
        "Curta", blank=True, related_name="favoritado_por"
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
        ordering = ["usuario__username"]

    def __str__(self):
        return f"{self.usuario} ({self.get_tipo_display()})"


# Modelo dos destaques da página "Comece por aqui"
class Destaque(models.Model):
    POSICAO_HORIZONTAL = [
        ("esquerda", "Esquerda"),
        ("centro", "Centro"),
        ("direita", "Direita"),
    ]

    POSICAO_VERTICAL = [
        ("topo", "Topo"),
        ("meio", "Meio"),
        ("baixo", "Baixo"),
    ]

    # Conteúdo

    titulo = models.CharField(max_length=200, blank=True)

    texto = models.TextField(blank=True)

    imagem = models.ImageField(upload_to="destaques/")

    # Cores do título e do texto

    cor_titulo = models.CharField(max_length=7, default="#FFFFFF")

    cor_texto = models.CharField(max_length=7, default="#FFFFFF")

    # Formatação do título e do texto

    titulo_negrito = models.BooleanField(default=False)

    titulo_italico = models.BooleanField(default=False)

    titulo_sublinhado = models.BooleanField(default=False)

    texto_negrito = models.BooleanField(default=False)

    texto_italico = models.BooleanField(default=False)

    texto_sublinhado = models.BooleanField(default=False)

    # Botão

    mostrar_botao = models.BooleanField(default=True)

    texto_botao = models.CharField(max_length=100, blank=True)

    link_botao = models.CharField(max_length=255, blank=True)

    # Cor do fundo do botão

    cor_fundo_botao = models.CharField(max_length=7, default="#FFFFFF")

    # Cor do texto do botão

    cor_texto_botao = models.CharField(max_length=7, default="#000000")

    # Borda do botão

    botao_com_borda = models.BooleanField(default=False)

    cor_borda_botao = models.CharField(max_length=7, default="#FFFFFF")

    # Formatação do botão

    botao_negrito = models.BooleanField(default=True)

    botao_italico = models.BooleanField(default=False)

    botao_sublinhado = models.BooleanField(default=False)

    # Posição do conteúdo

    posicao_horizontal = models.CharField(
        max_length=20, choices=POSICAO_HORIZONTAL, default="esquerda"
    )

    posicao_vertical = models.CharField(
        max_length=20, choices=POSICAO_VERTICAL, default="meio"
    )

    # Controle do destaque

    ativo = models.BooleanField(default=True)

    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Destaque"
        verbose_name_plural = "Destaques"
        ordering = ["ordem"]
        permissions = [
            (
                "pode_gerenciar_destaques",
                "Pode gerenciar destaques da página inicial",
            ),
        ]

    def __str__(self):
        return str(self.titulo) if self.titulo else f"Destaque {self.id}"


# Modelo dos cards "Aprenda. Crie. Conecte." da página "Comece por aqui"
class BlocoApresentacao(models.Model):
    # Conteúdo

    emoji = models.CharField(
        max_length=10, help_text="Emoji exibido no topo do card. Ex: 🎬"
    )

    texto = models.TextField(max_length=200)

    # Degradê da borda

    cor_gradiente_1 = models.CharField(max_length=7, default="#8b2ff7")

    cor_gradiente_2 = models.CharField(max_length=7, default="#22d3ee")

    # Controle do card

    ativo = models.BooleanField(default=True)

    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Bloco de apresentação"
        verbose_name_plural = "Blocos de apresentação"
        ordering = ["ordem"]

    def __str__(self):
        return str(self.texto)[:40] if self.texto else f"Bloco {self.id}"


# Modelo do texto da seção "Curtas em destaque"
class SecaoCurtas(models.Model):
    titulo = models.CharField(max_length=200, default="CURTAS EM DESTAQUE")

    subtitulo = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Texto da seção de curtas"
        verbose_name_plural = "Texto da seção de curtas"

    def __str__(self):
        return str(self.titulo)

    # Modelo dos curtas em destaque da página "Comece por aqui"


class Curta(models.Model):
    nome = models.CharField(max_length=200, default="Sem nome")

    grupo = models.CharField(
        max_length=150, blank=True, verbose_name="Nome do grupo"
    )

    cartaz = models.ImageField(upload_to="curtas/")

    link_youtube = models.URLField()

    cor_borda_1 = models.CharField(max_length=7, default="#7C3AED")

    cor_borda_2 = models.CharField(max_length=7, default="#06B6D4")

    ativo = models.BooleanField(default=True)

    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Curta em destaque"
        verbose_name_plural = "Curtas em destaque"
        ordering = ["ordem"]

    def __str__(self):
        return str(self.nome)


# Modelo do texto da seção final (chamada para ação)
class SecaoFinal(models.Model):
    titulo = models.CharField(
        max_length=200, default="PRONTO PARA DAR VIDA ÀS SUAS IDEIAS?"
    )

    subtitulo = models.TextField(blank=True)

    texto_botao = models.CharField(max_length=50, blank=True)

    link_botao = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Texto da seção final"
        verbose_name_plural = "Texto da seção final"

    def __str__(self):
        return str(self.titulo)

# Textos e imagens FIXOS (padrão) da página "Comece por aqui".
# Já nascem preenchidos; o admin pode alterar em "Textos das Seções".
class TextosHome(models.Model):
    # ---- Hero ----
    hero_titulo_leve = models.CharField("Hero: título (parte fina)", max_length=60, default="REDE")
    hero_titulo_forte = models.CharField("Hero: título (parte em negrito)", max_length=60, default="MIRADAS")
    hero_texto = models.TextField(
        "Hero: texto",
        default=(
            "Explore trilhas de aprendizagem, conheça produtoras parceiras "
            "e descubra projetos desenvolvidos por escolas."
        ),
    )
    hero_botao_texto = models.CharField("Hero: texto do botão", max_length=50, default="Saiba mais")
    hero_botao_link = models.CharField("Hero: link do botão", max_length=255, default="#aprenda")

    # ---- Aprenda. Crie. Conecte. ----
    aprenda_titulo = models.CharField("Aprenda: título", max_length=120, default="APRENDA. CRIE. CONECTE.")
    aprenda_texto = models.TextField(
        "Aprenda: texto",
        default=(
            "A Rede Miradas é uma plataforma dedicada à divulgação, "
            "valorização e votação de curtas-metragens, conectando "
            "estudantes, realizadores e espectadores em um espaço de "
            "criatividade, cultura e produção audiovisual."
        ),
    )
    aprenda_imagem = models.ImageField("Aprenda: ilustração (opcional)", upload_to="home/", blank=True, null=True)

    # ---- Trilhas ----
    trilhas_titulo = models.CharField("Trilhas: título", max_length=120, default="TRILHAS DE APRENDIZADO")
    trilhas_texto = models.TextField(
        "Trilhas: texto",
        default=(
            "Aprenda produção audiovisual em módulos práticos e criativos, "
            "do roteiro à edição final do seu curta."
        ),
    )
    trilhas_botao_texto = models.CharField("Trilhas: texto do botão", max_length=50, default="Visão geral das trilhas")
    trilhas_botao_link = models.CharField("Trilhas: link do botão", max_length=255, default="/trilhas/visao-geral/")
    trilhas_imagem = models.ImageField("Trilhas: ilustração (opcional)", upload_to="home/", blank=True, null=True)

    # ---- Selos ----
    selos_titulo = models.CharField("Selos: título", max_length=120, default="SELOS MIRADAS")
    selos_texto = models.TextField(
        "Selos: texto",
        default=(
            "Explore e encontre selos escondido pelo Rede miradas, cada "
            "selo traz um curta metragem que marcou a edição."
        ),
    )
    selos_botao_texto = models.CharField("Selos: texto do botão", max_length=50, default="Ver selos")
    selos_botao_link = models.CharField("Selos: link do botão", max_length=255, default="/perfil/")
    selos_imagem = models.ImageField("Selos: ilustração (opcional)", upload_to="home/", blank=True, null=True)

    # ---- Júri popular ----
    juri_titulo = models.CharField("Júri: título", max_length=120, default="JÚRI POPULAR")
    juri_texto = models.TextField(
        "Júri: texto",
        default=(
            "Durante a época de votação, você vai poder escolher seus "
            "curtas favoritos direto por aqui e ajudar a eleger o "
            "vencedor do júri popular."
        ),
    )
    juri_botao_texto = models.CharField("Júri: texto do botão", max_length=50, default="VER PARTICIPANTES")
    juri_botao_link = models.CharField("Júri: link do botão", max_length=255, default="/votacao/")

    # ---- Notícias ----
    noticias_titulo = models.CharField("Notícias: título", max_length=120, default="ACOMPANHE NOTÍCIAS")
    noticias_texto = models.TextField(
        "Notícias: texto",
        default="fique por dentro de tudo que rola por aqui, datas, vencedores e troféus",
    )
    noticias_botao_texto = models.CharField("Notícias: texto do botão", max_length=50, default="Página de notícias")
    noticias_botao_link = models.CharField("Notícias: link do botão", max_length=255, default="/noticias/")
    noticias_imagem = models.ImageField("Notícias: ilustração (opcional)", upload_to="home/", blank=True, null=True)

    class Meta:
        verbose_name = "Textos fixos da página inicial"
        verbose_name_plural = "Textos fixos da página inicial"

    def __str__(self):
        return "Textos da página inicial"

# Modelo das notícias do blog
class Noticia(models.Model):
    CATEGORIAS = [
        ("resultado", "Resultado"),
        ("evento", "Evento"),
        ("projeto", "Projeto"),
        ("novidade", "Novidade"),
        ("outros", "Outros"),
    ]

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS)
    resumo = models.TextField(max_length=300)
    texto = CKEditor5Field("Texto", config_name="default")
    imagem = models.ImageField(upload_to="noticias/")
    data_publicacao = models.DateTimeField(auto_now_add=True)

    destaque = models.BooleanField(default=False)
    destaque_secundario = models.BooleanField(
        default=False,
        help_text=(
            "Aparece na seção de destaques abaixo dos posts recentes. "
            'Não entra mais na lista de "Últimas notícias".'
        ),
    )

    publicada = models.BooleanField(default=True)

    # Cor de fundo usada quando a notícia está marcada como destaque
    cor_fundo_destaque = models.CharField(
        max_length=7,
        default="#3A1660",
        help_text="Cor de fundo exibida na seção de destaque.",
    )

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ["-data_publicacao", "-id"]
        permissions = [
            ("pode_publicar_noticia", "Pode publicar notícias"),
            ("pode_destacar_noticia", "Pode destacar notícias"),
        ]

    def __str__(self):
        return str(self.titulo)


# Modelos da Página Inicial das Trilhas de Aprendizagem


class TrilhasHero(models.Model):
    # Textos
    titulo = models.CharField(
        max_length=200, default="Bem-Vindo(a)", blank=True
    )

    subtitulo = models.TextField(
        default=(
            "Aprenda produção audiovisual em módulos práticos e criativos."
        ),
        blank=True,
    )

    imagem_fundo = models.ImageField(
        upload_to="trilhas/hero/",
        blank=True,
        null=True,
        help_text=(
            "Opcional. Se não enviada, mantém o fundo escuro com neon."
        ),
    )

    # Botão
    mostrar_botao = models.BooleanField(default=True)

    texto_botao = models.CharField(
        max_length=100, default="Conheça as trilhas", blank=True
    )

    link_botao = models.CharField(
        max_length=255, default="/trilhas/visao-geral/", blank=True
    )

    # Cores
    cor_titulo = models.CharField(max_length=7, default="#FFFFFF")

    cor_subtitulo = models.CharField(max_length=7, default="#FFFFFF")

    cor_fundo_botao = models.CharField(max_length=7, default="#FFFFFF")

    cor_texto_botao = models.CharField(max_length=7, default="#0B0C10")

    cor_glow_1 = models.CharField(
        max_length=7,
        default="#7C3AED",
        help_text="Cor primária do brilho neon central",
    )

    cor_glow_2 = models.CharField(
        max_length=7,
        default="#22D3EE",
        help_text="Cor secundária do brilho neon central",
    )

    # Formatação
    titulo_negrito = models.BooleanField(default=True)

    titulo_italico = models.BooleanField(default=False)

    subtitulo_negrito = models.BooleanField(default=False)

    subtitulo_italico = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Trilhas - Seção de Boas-Vindas (Hero)"
        verbose_name_plural = "Trilhas - Seção de Boas-Vindas (Hero)"

    def __str__(self):
        return str(self.titulo or "Seção de Boas-Vindas")


class TrilhasFaixaItem(models.Model):
    texto = models.CharField(
        max_length=100,
        help_text="Ex: 5 ETAPAS, MATERIAIS, EXERCÍCIOS, EXEMPLOS REAIS",
    )

    ordem = models.PositiveIntegerField(default=0)

    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Trilhas - Item da Faixa Informativa"
        verbose_name_plural = "Trilhas - Itens da Faixa Informativa"
        ordering = ["ordem"]

    def __str__(self):
        return str(self.texto)


class TrilhasCard(models.Model):
    CHOICES_ICONE = [
        ("equipes", "Aperto de mão (Equipes)"),
        ("texto", "Livro aberto (Texto Autoral)"),
        ("roteiro", "Lápis (Roteiro)"),
        ("producao", "Câmera de Cinema (Produção e Gravação)"),
        ("edicao", "Ilha de Edição e Corte (Edição e Finalização)"),
        ("personalizado", "Imagem / SVG personalizado"),
    ]

    CHOICES_BORDA = [
        ("dashed", "Tracejada"),
        ("solid", "Sólida"),
        ("dotted", "Pontilhada"),
        ("none", "Sem borda"),
    ]

    # Conteúdo
    tag = models.CharField(
        max_length=100, help_text="Ex: INSCRIÇÃO DAS EQUIPES"
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="Identificador único da URL, ex: inscricao-das-equipes",
    )

    titulo = models.CharField(
        max_length=250,
        help_text="Ex: Toda grande produção começa com uma boa equipe.",
    )

    titulo_detalhe = models.CharField(
        max_length=250,
        blank=True,
        default="",
        help_text=(
            "Título exibido no topo da página de detalhes "
            "(ex: INSCRIÇÃO DAS EQUIPES: IDENTIDADE VISUAL)"
        ),
    )

    descricao = models.TextField(
        help_text="Ex: Conheça a ficha de inscrição, apresente sua equipe..."
    )

    # Imagem de capa do Card (estilo Substack / Figma)
    imagem_capa = models.ImageField(
        upload_to="trilhas/capas/",
        blank=True,
        null=True,
        help_text="Imagem de capa ilustrativa do card da trilha",
    )

    # Ícone
    tipo_icone = models.CharField(
        max_length=30,
        choices=CHOICES_ICONE,
        default="equipes",
        help_text="Selecione o ícone ilustrado padrão ou envie imagem própria",
    )

    icone_personalizado = models.ImageField(
        upload_to="trilhas/icones/",
        blank=True,
        null=True,
        help_text=(
            "Opcional. Imagem ou SVG caso tenha selecionado ícone próprio"
        ),
    )

    # Botão
    mostrar_botao = models.BooleanField(default=True)

    texto_botao = models.CharField(
        max_length=100, default="Começar", blank=True
    )

    link_botao = models.CharField(
        max_length=255, default="/trilhas/visao-geral/", blank=True
    )

    # Cores
    cor_fundo_card = models.CharField(
        max_length=7, default="#101535", help_text="Cor de fundo do card"
    )

    cor_borda_card = models.CharField(
        max_length=7, default="#1E2659", help_text="Cor da borda do card"
    )

    estilo_borda = models.CharField(
        max_length=20, choices=CHOICES_BORDA, default="solid"
    )

    cor_glow = models.CharField(
        max_length=7,
        default="#7C3AED",
        help_text="Cor do brilho neon no fundo do card",
    )

    cor_tag = models.CharField(
        max_length=7, default="#94A3B8", help_text="Cor da tag superior"
    )

    cor_titulo = models.CharField(
        max_length=7, default="#FFFFFF", help_text="Cor do título"
    )

    cor_descricao = models.CharField(
        max_length=7, default="#CBD5E1", help_text="Cor da descrição"
    )

    cor_fundo_botao = models.CharField(
        max_length=7, default="#B94B61", help_text="Cor de fundo do botão"
    )

    cor_texto_botao = models.CharField(
        max_length=7, default="#FFFFFF", help_text="Cor do texto do botão"
    )

    cor_sidebar = models.CharField(
        max_length=7,
        default="#8F3D4E",
        help_text="Cor de fundo da barra lateral na página de detalhes",
    )

    cor_sidebar_topo = models.CharField(
        max_length=7,
        default="#BA586C",
        help_text="Cor de fundo do box superior da barra lateral",
    )

    # Formatação de fontes
    tag_negrito = models.BooleanField(default=True)

    tag_italico = models.BooleanField(default=False)

    titulo_negrito = models.BooleanField(default=True)

    titulo_italico = models.BooleanField(default=False)

    descricao_negrito = models.BooleanField(default=False)

    descricao_italico = models.BooleanField(default=False)

    # Controle
    ativo = models.BooleanField(default=True)

    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Trilhas - Card de Trilha"
        verbose_name_plural = "Trilhas - Cards de Trilhas"
        ordering = ["ordem"]
        permissions = [
            ("pode_gerenciar_trilhas", "Pode gerenciar trilhas de aprendizagem"),
        ]

    def __str__(self):
        return f"{self.tag} - {str(self.titulo)[:30]}"


class SubtopicoTrilha(models.Model):
    trilha = models.ForeignKey(
        TrilhasCard, on_delete=models.CASCADE, related_name="subtopicos"
    )

    titulo = models.CharField(
        max_length=255,
        help_text="Título do item/subtópico. Ex: CONTO e CRÔNICA",
    )

    link = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text=(
            "Link específico para a aula (opcional). Se vazio, "
            "usará o link da trilha."
        ),
    )

    mostrar_botao_comecar = models.BooleanField(
        default=False, help_text='Exibir o botão "Começar" ao lado deste item'
    )

    ordem = models.PositiveIntegerField(default=0)

    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Subtópico da Trilha"
        verbose_name_plural = "Subtópicos da Trilha"
        ordering = ["ordem"]

    def __str__(self):
        return f"{self.trilha.titulo} - {self.titulo}"


class UnidadeTrilha(models.Model):
    trilha = models.ForeignKey(
        TrilhasCard, on_delete=models.CASCADE, related_name="unidades"
    )

    numero = models.PositiveIntegerField(
        default=1, verbose_name="Número da Unidade (ex: 1, 2, 3...)"
    )

    titulo = models.CharField(
        max_length=200,
        help_text="Nome da unidade (ex: Identidade Visual ou Conto e Crônica)",
    )

    ordem = models.PositiveIntegerField(default=0)

    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Trilhas - Unidade da Trilha"
        verbose_name_plural = "Trilhas - Unidades das Trilhas"
        ordering = ["ordem", "numero"]

    def __str__(self):
        nome_trilha = self.trilha.tag or self.trilha.titulo
        return f"{nome_trilha} - Unidade {self.numero}: {self.titulo}"


class TopicoUnidadeTrilha(models.Model):
    unidade = models.ForeignKey(
        UnidadeTrilha, on_delete=models.CASCADE, related_name="topicos"
    )

    titulo = models.CharField(
        max_length=250,
        help_text="Título da aula/conteúdo (ex: Como fazer roteiro?)",
    )

    conteudo = CKEditor5Field(
        "Conteúdo (Texto / Formatação)", config_name="default", blank=True
    )

    ordem = models.PositiveIntegerField(default=0)

    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Trilhas - Tópico / Conteúdo da Unidade"
        verbose_name_plural = "Trilhas - Tópicos / Conteúdos das Unidades"
        ordering = ["ordem"]

    def __str__(self):
        return f"Unidade {self.unidade.numero} - {self.titulo}"
