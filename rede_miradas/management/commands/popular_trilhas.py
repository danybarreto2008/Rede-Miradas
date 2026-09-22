from django.core.management.base import BaseCommand
from rede_miradas.models import TrilhasCard, SubtopicoTrilha


class Command(BaseCommand):
    help = 'Popula as 5 Trilhas de Aprendizagem e seus subtópicos reais com ícones específicos'

    def handle(self, *args, **options):
        dados_trilhas = [
            {
                'tag': 'Etapa 1',
                'titulo': 'Inscrição das equipes',
                'descricao': 'Apresentação dos participantes, formação dos grupos e identidade visual do projeto.',
                'imagem_capa': 'trilhas/capas/capa_equipes.jpg',
                'tipo_icone': 'equipes',
                'ordem': 1,
                'cor_fundo_card': '#0c102a',
                'cor_borda_card': '#f97316',
                'cor_glow': '#ea580c',
                'cor_tag': '#fdba74',
                'subtopicos': [
                    ('Apresentação das equipes', True),
                    ('Inscrição das equipes', False),
                    ('Identidade Visual: Como fazer?', False),
                    ('Ficha de Inscrição e funções da equipe', False),
                ]
            },
            {
                'tag': 'Etapa 2',
                'titulo': 'Texto autoral',
                'descricao': 'Da leitura à criação: conto, crônica e narrativa autoral para o curta.',
                'imagem_capa': 'trilhas/capas/capa_texto_autoral.jpg',
                'tipo_icone': 'texto',
                'ordem': 2,
                'cor_fundo_card': '#0c102a',
                'cor_borda_card': '#8b5cf6',
                'cor_glow': '#7c3aed',
                'cor_tag': '#c4b5fd',
                'subtopicos': [
                    ('CONTO e CRÔNICA: como diferenciar?', True),
                    ('Crônicas finalistas da Olimpíada Nacional de Língua Portuguesa', False),
                    ('Lá na minha terra', False),
                    ('Quebra-molas', False),
                    ('A perca', False),
                    ('Crônicas de Paris', False),
                    ('Isso é ser brasileiro!', False),
                    ('Varal de Sonhos', False),
                ]
            },
            {
                'tag': 'Etapa 3',
                'titulo': 'Roteiro',
                'descricao': 'Transforme suas ideias e textos em roteiro cinematográfico com cenas e diálogos.',
                'imagem_capa': 'trilhas/capas/capa_roteiro.jpg',
                'tipo_icone': 'roteiro',
                'ordem': 3,
                'cor_fundo_card': '#0c102a',
                'cor_borda_card': '#0ea5e9',
                'cor_glow': '#0284c7',
                'cor_tag': '#7dd3fc',
                'subtopicos': [
                    ('O que é um roteiro audiovisual e estrutura narrativa', True),
                    ('Da ideia à escaleta: organizando os acontecimentos', False),
                    ('Formatação padrão de roteiro e cabeçalho de cena', False),
                    ('Construção de personagens e diálogos naturais', False),
                    ('Decupagem do roteiro: preparando o plano de filmagem', False),
                ]
            },
            {
                'tag': 'Etapa 4',
                'titulo': 'Produção e Gravação',
                'descricao': 'Técnicas práticas de filmagem, planos de câmera, áudio e iluminação no set.',
                'imagem_capa': 'trilhas/capas/capa_producao_gravacao.jpg',
                'tipo_icone': 'producao',
                'ordem': 4,
                'cor_fundo_card': '#0c102a',
                'cor_borda_card': '#10b981',
                'cor_glow': '#059669',
                'cor_tag': '#6ee7b7',
                'subtopicos': [
                    ('Planejamento de filmagem e lista de necessidades', True),
                    ('Planos, enquadramentos e movimentos de câmera', False),
                    ('Iluminação básica: 3 pontos e luz natural', False),
                    ('Captação de áudio limpo no set de gravação', False),
                    ('Direção de atores e condução das gravações', False),
                ]
            },
            {
                'tag': 'Etapa 5',
                'titulo': 'Edição e Finalização',
                'descricao': 'Montagem, ritmo de corte, trilha sonora, efeitos e exportação para a grande tela.',
                'imagem_capa': 'trilhas/capas/capa_edicao_finalizacao.jpg',
                'tipo_icone': 'edicao',
                'ordem': 5,
                'cor_fundo_card': '#0c102a',
                'cor_borda_card': '#f43f5e',
                'cor_glow': '#e11d48',
                'cor_tag': '#fda4af',
                'subtopicos': [
                    ('Organização do material bruto e seleção dos melhores takes', True),
                    ('Montagem no editor de vídeo: ritmo, continuidade e cortes', False),
                    ('Trilha sonora, efeitos de som e mixagem de áudio', False),
                    ('Correção de cor e efeitos visuais', False),
                    ('Exportação final e exibição do curta-metragem', False),
                ]
            },
        ]

        TrilhasCard.objects.all().delete()

        for dados in dados_trilhas:
            subtopicos = dados.pop('subtopicos')
            card = TrilhasCard.objects.create(
                tag=dados['tag'],
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
                cor_titulo='#FFFFFF',
                cor_descricao='#CBD5E1',
                cor_fundo_botao='#B94B61',
                cor_texto_botao='#FFFFFF',
                texto_botao='Começar',
                link_botao='/trilhas/visao-geral/',
                ativo=True
            )

            for idx, (sub_titulo, mostrar_btn) in enumerate(subtopicos, start=1):
                SubtopicoTrilha.objects.create(
                    trilha=card,
                    titulo=sub_titulo,
                    mostrar_botao_comecar=mostrar_btn,
                    ordem=idx,
                    ativo=True
                )

        self.stdout.write(self.style.SUCCESS('5 Trilhas e seus subtópicos cadastrados com sucesso!'))
