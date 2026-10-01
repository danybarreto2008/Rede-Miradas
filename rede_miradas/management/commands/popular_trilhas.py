from django.core.management.base import BaseCommand
from rede_miradas.models import (
    TrilhasCard, SubtopicoTrilha, TrilhasHero, TrilhasFaixaItem,
    UnidadeTrilha, TopicoUnidadeTrilha
)


class Command(BaseCommand):
    help = 'Popula as 5 Trilhas de Aprendizagem, subtópicos, unidades, Hero e Faixa informativa'

    def handle(self, *args, **options):
        # 1. Popula Seção Hero se não existir
        if not TrilhasHero.objects.exists():
            TrilhasHero.objects.create(
                titulo='Bem-Vindo(a)',
                subtitulo='Aprenda produção audiovisual em módulos práticos e criativos.',
                mostrar_botao=True,
                texto_botao='Conheça as trilhas',
                link_botao='/trilhas/visao-geral/',
                cor_titulo='#FFFFFF',
                cor_subtitulo='#FFFFFF',
                cor_fundo_botao='#FFFFFF',
                cor_texto_botao='#0B0C10',
                cor_glow_1='#7C3AED',
                cor_glow_2='#22D3EE',
                titulo_negrito=True,
            )
            self.stdout.write(self.style.SUCCESS('Hero das Trilhas cadastrado.'))

        # 2. Popula Itens da Faixa Informativa se não existirem
        if not TrilhasFaixaItem.objects.exists():
            itens_faixa = [
                '5 ETAPAS',
                'DEZENAS DE MATERIAIS',
                'EXERCÍCIOS',
                'EXEMPLOS REAIS',
            ]
            for idx, txt in enumerate(itens_faixa, start=1):
                TrilhasFaixaItem.objects.create(texto=txt, ordem=idx, ativo=True)
            self.stdout.write(self.style.SUCCESS('Itens da Faixa informativa cadastrados.'))

        # 3. Popula os 5 Cards de Trilhas e Subtópicos
        dados_trilhas = [
            {
                'tag': 'Etapa 1',
                'slug': 'inscricao-das-equipes',
                'titulo': 'Inscrição das equipes',
                'descricao': 'Apresentação dos participantes, formação dos grupos e identidade visual do projeto.',
                'imagem_capa': 'trilhas/capas/capa_equipes.jpg',
                'tipo_icone': 'equipes',
                'ordem': 1,
                'cor_fundo_card': '#0c102a',
                'cor_borda_card': '#f97316',
                'cor_glow': '#ea580c',
                'cor_tag': '#fdba74',
                'cor_sidebar': '#8F3D4E',
                'cor_sidebar_topo': '#BA586C',
                'link_botao': '/trilhas/inscricao-das-equipes/',
                'subtopicos': [
                    ('Identidade visual', '/trilhas/inscricao-das-equipes/#unidade-1', True),
                    ('Ficha de inscrição', '/trilhas/inscricao-das-equipes/#unidade-2', False),
                ]
            },
            {
                'tag': 'Etapa 2',
                'slug': 'texto-autoral',
                'titulo': 'Texto autoral',
                'descricao': 'Da leitura à criação: conto, crônica e narrativa autoral para o curta.',
                'imagem_capa': 'trilhas/capas/capa_texto_autoral.jpg',
                'tipo_icone': 'texto',
                'ordem': 2,
                'cor_fundo_card': '#0c102a',
                'cor_borda_card': '#8b5cf6',
                'cor_glow': '#7c3aed',
                'cor_tag': '#c4b5fd',
                'link_botao': '/trilhas/texto-autoral/',
                'subtopicos': [
                    ('CONTO e CRÔNICA: como diferenciar?', '/trilhas/texto-autoral/#unidade-1', True),
                    ('Crônicas finalistas da Olimpíada Nacional de Língua Portuguesa', '/trilhas/texto-autoral/#unidade-2', False),
                    ('Lá na minha terra', '/trilhas/texto-autoral/#unidade-3', False),
                    ('Quebra-molas', '/trilhas/texto-autoral/#unidade-4', False),
                    ('A perca', '/trilhas/texto-autoral/#unidade-5', False),
                    ('Crônicas de Paris', '/trilhas/texto-autoral/#unidade-6', False),
                    ('Isso é ser brasileiro!', '/trilhas/texto-autoral/#unidade-7', False),
                    ('Varal de Sonhos', '/trilhas/texto-autoral/#unidade-8', False),
                ]
            },
            {
                'tag': 'Etapa 3',
                'slug': 'roteiro',
                'titulo': 'Roteiro',
                'descricao': 'Transforme suas ideias e textos em roteiro cinematográfico com cenas e diálogos.',
                'imagem_capa': 'trilhas/capas/capa_roteiro.jpg',
                'tipo_icone': 'roteiro',
                'ordem': 3,
                'cor_fundo_card': '#0c102a',
                'cor_borda_card': '#0ea5e9',
                'cor_glow': '#0284c7',
                'cor_tag': '#7dd3fc',
                'link_botao': '/trilhas/roteiro/',
                'subtopicos': [
                    ('O que é um roteiro audiovisual e estrutura narrativa', '/trilhas/roteiro/#unidade-1', True),
                    ('Da ideia à escaleta: organizando os acontecimentos', '/trilhas/roteiro/#unidade-2', False),
                    ('Formatação padrão de roteiro e cabeçalho de cena', '/trilhas/roteiro/#unidade-3', False),
                    ('Construção de personagens e diálogos naturais', '/trilhas/roteiro/#unidade-4', False),
                    ('Decupagem do roteiro: preparando o plano de filmagem', '/trilhas/roteiro/#unidade-5', False),
                ]
            },
            {
                'tag': 'Etapa 4',
                'slug': 'producao-e-gravacao',
                'titulo': 'Produção e Gravação',
                'descricao': 'Técnicas práticas de filmagem, planos de câmera, áudio e iluminação no set.',
                'imagem_capa': 'trilhas/capas/capa_producao_gravacao.jpg',
                'tipo_icone': 'producao',
                'ordem': 4,
                'cor_fundo_card': '#0c102a',
                'cor_borda_card': '#10b981',
                'cor_glow': '#059669',
                'cor_tag': '#6ee7b7',
                'link_botao': '/trilhas/producao-e-gravacao/',
                'subtopicos': [
                    ('Planejamento de filmagem e lista de necessidades', '/trilhas/producao-e-gravacao/#unidade-1', True),
                    ('Planos, enquadramentos e movimentos de câmera', '/trilhas/producao-e-gravacao/#unidade-2', False),
                    ('Iluminação básica: 3 pontos e luz natural', '/trilhas/producao-e-gravacao/#unidade-3', False),
                    ('Captação de áudio limpo no set de gravação', '/trilhas/producao-e-gravacao/#unidade-4', False),
                    ('Direção de atores e condução das gravações', '/trilhas/producao-e-gravacao/#unidade-5', False),
                ]
            },
            {
                'tag': 'Etapa 5',
                'slug': 'edicao-e-finalizacao',
                'titulo': 'Edição e Finalização',
                'descricao': 'Montagem, ritmo de corte, trilha sonora, efeitos e exportação para a grande tela.',
                'imagem_capa': 'trilhas/capas/capa_edicao_finalizacao.jpg',
                'tipo_icone': 'edicao',
                'ordem': 5,
                'cor_fundo_card': '#0c102a',
                'cor_borda_card': '#f43f5e',
                'cor_glow': '#e11d48',
                'cor_tag': '#fda4af',
                'link_botao': '/trilhas/edicao-e-finalizacao/',
                'subtopicos': [
                    ('Organização do material bruto e seleção dos melhores takes', '/trilhas/edicao-e-finalizacao/#unidade-1', True),
                    ('Montagem no editor de vídeo: ritmo, continuidade e cortes', '/trilhas/edicao-e-finalizacao/#unidade-2', False),
                    ('Trilha sonora, efeitos de som e mixagem de áudio', '/trilhas/edicao-e-finalizacao/#unidade-3', False),
                    ('Correção de cor e efeitos visuais', '/trilhas/edicao-e-finalizacao/#unidade-4', False),
                    ('Exportação final e exibição do curta-metragem', '/trilhas/edicao-e-finalizacao/#unidade-5', False),
                ]
            },
        ]

        TrilhasCard.objects.all().delete()

        for dados in dados_trilhas:
            subtopicos = dados.pop('subtopicos')
            card = TrilhasCard.objects.create(
                tag=dados['tag'],
                slug=dados['slug'],
                titulo=dados['titulo'],
                descricao=dados['descricao'],
                imagem_capa=dados['imagem_capa'],
                tipo_icone=dados['tipo_icone'],
                ordem=dados['ordem'],
                cor_fundo_card=dados['cor_fundo_card'],
                cor_borda_card=dados['cor_borda_card'],
                estilo_borda='solid',
                cor_glow=dados['cor_glow'],
                cor_tag=dados['cor_tag'],
                cor_sidebar=dados.get('cor_sidebar', '#8F3D4E'),
                cor_sidebar_topo=dados.get('cor_sidebar_topo', '#BA586C'),
                cor_titulo='#FFFFFF',
                cor_descricao='#CBD5E1',
                cor_fundo_botao='#B94B61',
                cor_texto_botao='#FFFFFF',
                texto_botao='Começar',
                link_botao=dados['link_botao'],
                ativo=True
            )

            for idx, (sub_titulo, sub_link, mostrar_btn) in enumerate(subtopicos, start=1):
                SubtopicoTrilha.objects.create(
                    trilha=card,
                    titulo=sub_titulo,
                    link=sub_link,
                    mostrar_botao_comecar=mostrar_btn,
                    ordem=idx,
                    ativo=True
                )

            # Cadastra as Unidades e Tópicos da 1ª Trilha (Inscrição das equipes)
            if card.slug == 'inscricao-das-equipes':
                un1 = UnidadeTrilha.objects.create(
                    trilha=card,
                    numero=1,
                    titulo='Identidade Visual',
                    ordem=1,
                    ativo=True
                )

                conteudo_un1 = """<p>O logotipo deveria ser o princípio de todo grande projeto: pode parecer banal, mas a identidade visual é como uma bandeira que une a equipe no mesmo propósito. A seguir deixei alguns links com dicas para construir uma boa logo, porém não é obrigatório começar do zero se você não tem talento pra desenho ou recursos tecnológicos para criar. O último link leva você direto para o Canva e sua seção de criação de logos: escolha uma que represente os sentimentos que a equipe quer expressar e personalize o que for possível.</p>

<div class="trilha-links-secao">
    <div class="trilha-links-titulo">
        <i class="bi bi-tools me-2"></i> Links e ferramentas para criar sua logo:
    </div>
    <div class="trilha-resource-cards-grid">
        <a href="https://www.canva.com/pt_br/logos/" target="_blank" rel="noopener noreferrer" class="trilha-resource-card card-canva">
            <div class="resource-card-left">
                <div class="resource-card-icon icon-canva"><i class="bi bi-brush-fill"></i></div>
                <div class="resource-card-info">
                    <span class="resource-card-badge badge-destaque">Canva Logos</span>
                    <span class="resource-card-name">Canva: Criar Logotipo</span>
                    <span class="resource-card-domain">canva.com/pt_br/logos</span>
                </div>
            </div>
            <div class="resource-card-action">Acessar <i class="bi bi-box-arrow-up-right"></i></div>
        </a>
        <a href="https://www.tailorbrands.com/pt-br/logo-maker/como-criar-um-logotipo/dicas-de-design-de-logotipo" target="_blank" rel="noopener noreferrer" class="trilha-resource-card card-tailor">
            <div class="resource-card-left">
                <div class="resource-card-icon icon-tailor"><i class="bi bi-palette-fill"></i></div>
                <div class="resource-card-info">
                    <span class="resource-card-badge">Dicas de Design</span>
                    <span class="resource-card-name">Tailor Brands: Dicas de Logotipo</span>
                    <span class="resource-card-domain">tailorbrands.com</span>
                </div>
            </div>
            <div class="resource-card-action">Acessar <i class="bi bi-box-arrow-up-right"></i></div>
        </a>
        <a href="https://www.godaddy.com/resources/br/artigos/como-fazer-logotipo" target="_blank" rel="noopener noreferrer" class="trilha-resource-card card-godaddy">
            <div class="resource-card-left">
                <div class="resource-card-icon icon-godaddy"><i class="bi bi-lightning-charge-fill"></i></div>
                <div class="resource-card-info">
                    <span class="resource-card-badge">Artigo Prático</span>
                    <span class="resource-card-name">GoDaddy: Como Fazer Logotipo</span>
                    <span class="resource-card-domain">godaddy.com</span>
                </div>
            </div>
            <div class="resource-card-action">Acessar <i class="bi bi-box-arrow-up-right"></i></div>
        </a>
        <a href="https://criativito.com.br/11-dicas-importantes-para-voce-criar-um-logo-profissional/" target="_blank" rel="noopener noreferrer" class="trilha-resource-card card-criativito">
            <div class="resource-card-left">
                <div class="resource-card-icon icon-criativito"><i class="bi bi-stars"></i></div>
                <div class="resource-card-info">
                    <span class="resource-card-badge">Guia Profissional</span>
                    <span class="resource-card-name">Criativito: 11 Dicas Importantes</span>
                    <span class="resource-card-domain">criativito.com.br</span>
                </div>
            </div>
            <div class="resource-card-action">Acessar <i class="bi bi-box-arrow-up-right"></i></div>
        </a>
    </div>
</div>"""

                TopicoUnidadeTrilha.objects.create(
                    unidade=un1,
                    titulo='Identidade visual da equipe: como fazer?',
                    conteudo=conteudo_un1,
                    ordem=1,
                    ativo=True
                )

                un2 = UnidadeTrilha.objects.create(
                    trilha=card,
                    numero=2,
                    titulo='Ficha de Inscrição',
                    ordem=2,
                    ativo=True
                )

                conteudo_un2 = """<p>A inscrição da equipe deverá ser realizada por meio do formulário disponibilizado pela instituição durante o período do festival. Cada equipe deverá preencher apenas uma ficha de inscrição, contendo todas as informações solicitadas.</p>"""

                TopicoUnidadeTrilha.objects.create(
                    unidade=un2,
                    titulo='Ficha de Inscrição',
                    conteudo=conteudo_un2,
                    ordem=1,
                    ativo=True
                )

        self.stdout.write(self.style.SUCCESS('5 Trilhas, subtópicos e Unidades de Inscrição cadastradas com sucesso!'))

