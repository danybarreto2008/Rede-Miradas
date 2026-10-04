import os
import shutil
from pathlib import Path
from django.conf import settings
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

        # Garante que as imagens de capa padrão de static sejam copiadas para a pasta media/ se necessário
        static_trilhas_dir = Path(settings.BASE_DIR) / 'rede_miradas' / 'static' / 'rede_miradas' / 'img' / 'trilhas'
        media_capas_dir = Path(settings.MEDIA_ROOT) / 'trilhas' / 'capas'
        media_capas_dir.mkdir(parents=True, exist_ok=True)

        TrilhasCard.objects.all().delete()

        for dados in dados_trilhas:
            img_rel = dados.get('imagem_capa')
            if img_rel:
                nome_arquivo = Path(img_rel).name
                src_img = static_trilhas_dir / nome_arquivo
                dest_img = Path(settings.MEDIA_ROOT) / img_rel
                if src_img.exists() and not dest_img.exists():
                    shutil.copy2(src_img, dest_img)
                    self.stdout.write(self.style.SUCCESS(f'Capa copiada para mídia: {nome_arquivo}'))

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

            # Cadastra as Unidades e Tópicos da 2ª Trilha (Texto autoral)
            if card.slug == 'texto-autoral':
                # Unidade 1
                un1 = UnidadeTrilha.objects.create(
                    trilha=card,
                    numero=1,
                    titulo='CONTO e CRÔNICA: como diferenciar?',
                    ordem=1,
                    ativo=True
                )

                conteudo_un1 = """<p>Nesta edição, os curtas-metragens serão produzidos a partir de uma crônica ou de um conto autorais da equipe. Por isso, é necessário entender como funcionam os dois gêneros.</p>
<p>Leia a seguir os CONTOS intitulados <em>"Dizem que os cães vêem coisas"</em>, de Moreira Campos, e <em>"A moça tecelã"</em>, de Marina Colassanti, e anote as diferenças que você observou entre esses textos e as crônicas lidas anteriormente.</p>

<div class="trilha-leitura-box">
    <div class="trilha-leitura-header">
        <h4 class="trilha-leitura-title"><i class="bi bi-book me-2"></i> CONTO: Dizem que os cães vêem coisas</h4>
        <p class="trilha-leitura-autor">Por Moreira Campos</p>
    </div>
    <div class="trilha-leitura-corpo">
        <p>Ela chegou diáfana, transparente, no vestido branco que lhe descia até os pés calçados pelas ricas sandálias de pluma. Ninguém lhe ouviu os passos. Sentou-se à beira da grande piscina, cruzando as pernas longas. Chegou antiqüíssima, atual e eterna, com a sua cara de máscara. Moldada em gesso? Apenas uma presença, porque pousou como uma sombra. Mas por um fragmento de tempo, um quase nada, reinou entre todos um silêncio largo, que se estendeu pelo vasto terreno murado da mansão ensombrada pelas árvores, dominou a enorme piscina e emudeceu as próprias crianças pajeadas pelas babás de aventais bordados, e vejam que as crianças são indóceis.</p>
        <p>Um presságio.</p>
        <p>Fragmento de tempo apenas, porque o homem gordo, de ventre imenso, saltou dentro da piscina com o copo de uísque na mão. Espadanou água por todos os lados, a piscina transbordou. Muitos se molharam, outros saltaram da cadeira de lona.</p>
        <p>— Bruto! – disse alguém íntimo, sem que ele se aborrecesse, bêbado.</p>
        <p>A onda de água despejou-se sobre Ela, que não se moveu: era trespassável e transparente. Floco de névoa pronto a esvoaçar. Permaneceu parada, a cara imóvel, nenhum ricto. Apenas parecia consultar no pulso um relógio invisível, para marcar o tempo. O homem de ventre enorme já estava à beira da piscina, gotejante e trôpego, para uma nova dose de uísque, os dedos graúdos catando no balde os cubos de gelo. Mulheres seminuas, o cordão do biquíni, as nádegas reluzentes de sol e gotas d'água. As rodas, as conversas, os garçons que circulavam, as bandejas de salgadinhos.</p>
        <p>Uns óculos escuros sofisticados no sutiã mínimo:</p>
        <p>— Por favor.</p>
        <p>O garçom atendia, solícito, perdendo os olhos ávidos nos seios mal contidos, oferecidos e inatingíveis.</p>
        <p>— Obrigada.</p>
        <p>O garçom mantinha a dignidade, ereto. A menina chegou e segurou a mãe pelo queixo:</p>
        <p>— Mãe-ê, quero uma coca-cola.</p>
        <p>A mãe não lhe dava atenção em flerte com o recente campeão de vôlei, uma estrutura de tórax (a mãe da menina contrariava-se apenas com o tufo de pelos que ele tinha no peito, quase imoral). A menina impacientava-se:</p>
        <p>— Mãe-ê, uma coca-cola.</p>
        <p>— Deixa de ser chata!</p>
        <p>O campeão levantou-se para apanhar o refrigerante. Em roda mais distante conversavam os homens graves: a última medida do governo, a crise econômica.</p>
        <p>— O país vai à bancarrota.</p>
        <p>— Vai o quê?</p>
        <p>— A bancarrota.</p>
        <p>— Fazia tempo que eu não ouvia essa palavra.</p>
        <p>— Mas vai.</p>
        <p>Aceitava-se a bancarrota sem muita convicção. Na grande varanda, as senhoras grisalhas e indesnudáveis, pulseiras tilintantes na flacidez dos braços, discutiam os novos valores morais e comentavam o recente desquite.</p>
        <p>— A menina dela não tem um ano de casada.</p>
        <p>— É a segunda que se separa.</p>
        <p>— Como?</p>
        <p>— A segunda.</p>
        <p>Aniversário da dona da mansão, que se acompanhava ao violão com graça, aplaudida pelos que estavam em volta. O garçom (ou maitre, porque era solene) curvou-se ao seu ouvido. Ela se livrou do violão, levantou-se e bateu palmas chamando todos para o almoço à americana, as mesas sob as árvores. Cada um apanhou o seu prato, formaram-se as filas, o homem gentil cedeu lugar a umas nádegas rijas, cortadas sempre pelo cordão do biquíni:</p>
        <p>— Faz favor.</p>
        <p>— Obrigada.</p>
        <p>Os cães de raça latiam e uivavam desesperadamente nos canis (e dizem que os cães vêem coisas). Foi preciso que o tratador viesse acalmá-los, embora eles rodassem sobre si mesmos e rosnassem. À distância, a piscina quase olímpica, agora deserta: toalhas esquecidas. O vidro de bronzeador, o cinzeiro sobre a mesinha cheio de pontas de cigarro marcadas de batom.</p>
        <p>As filas. Alguém tangeu o gato que lutava com um pedaço de osso. Lenita fez o prato do marido, preparou também o seu. Mordia a fatia de peru com farofa, quando se lembrou do filho:</p>
        <p>— Cadê o Netinho?</p>
        <p>Certa angústia na voz. Chamou o marido, gritou pela babá, que se distraía com as outras na varanda. Olhos espantados e repentino silêncio talvez maior de qualquer outro. Refeições suspensas, uma senhora mantinha no ar o garfo cheio. Tentavam segurar Lenita. Ela se desvencilhava:</p>
        <p>— Cadê o Netinho? Cadê?</p>
        <p>As águas da grande piscina eram tranquilas, apenas levemente franjadas pelo vento. Boiava sobre elas uma carteira de cigarros vazia. Mas a moça que se aproximava parecia divisar um corpo no fundo, preso à escada. Voltaram a afastar Lenita, o marido a envolveu nos braços possantes, talvez procurando refúgio também. O campeão de vôlei atirou-se à piscina e veio à tona sacudindo com a cabeça os cabelos longos: trazia sob o braço um corpo inerme, flácido, de apenas quatro anos e de cabelos louros e gotejantes.</p>
        <p>O médico novo, de calção, tentou a respiração artificial, e boca-a-boca (os lábios de Netinho estavam arroxeados), e levantou-se sem palavras e sem olhar para ninguém. Lenita soltou-se e agarrou-se ao filho:</p>
        <p>— Acorde, acorde! Pelo amor de Deus, acorde!</p>
        <p>Conseguiram afastá-la mais de uma vez, quase desmaiou. A amiga limpava-lhe com os dedos a sobra de farofa que se grudava ao seu rosto. Os cães de raça voltavam a latir desesperadamente, e dizem que os cães vêem coisas.</p>
        <p>Lenita ficou para sempre com a sensação do corpo inerte e mole entre os braços. Uma marca, uma presença, que procurava desfazer com as mãos. Cabelos louros e gotejantes. Às vezes, ela despertava na noite:</p>
        <p>— Acorde, acorde!</p>
        <p>A presença também daquele instante de silêncio que pesara sobre a piscina. Um pressentimento apenas? Precisamente o momento em que Ela chegara, transparente e invisível, e se assentara à beira da piscina, cruzando as pernas longas, antiqüíssima, atual e eterna.</p>
    </div>
    <div class="trilha-leitura-rodape">
        CAMPOS, José Maria Moreira. <em>Dizem que os cães vêem coisas</em>. Fortaleza: Edições UFC, 1987.
    </div>
</div>

<div class="trilha-leitura-box">
    <div class="trilha-leitura-header">
        <h4 class="trilha-leitura-title"><i class="bi bi-book me-2"></i> CONTO: A moça tecelã</h4>
        <p class="trilha-leitura-autor">Por Marina Colasanti</p>
    </div>
    <div class="trilha-leitura-corpo">
        <p>Acordava ainda no escuro, como se ouvisse o sol chegando atrás das beiradas da noite. E logo sentava-se ao tear.</p>
        <p>Linha clara, para começar o dia. Delicado traço cor da luz, que ela ia passando entre os fios estendidos, enquanto lá fora a claridade da manhã desenhava o horizonte. Depois lãs mais vivas, quentes lãs iam tecendo hora a hora, em longo tapete que nunca acabava.</p>
        <p>Se era forte demais o sol, e no jardim pendiam as pétalas, a moça colocava na lançadeira grossos fios cinzentos do algodão mais felpudo. Em breve, na penumbra trazida pelas nuvens, escolhia um fio de prata, que em pontos longos rebordava sobre o tecido. Leve, a chuva vinha cumprimentá-la à janela.</p>
        <p>Mas se durante muitos dias o vento e o frio brigavam com as folhas e espantavam os pássaros, bastava a moça tecer com seus belos fios dourados, para que o sol voltasse a acalmar a natureza.</p>
        <p>Assim, jogando a lançadeira de um lado para outro e batendo os grandes pentes do tear para frente e para trás, a moça passava os seus dias.</p>
        <p>Nada lhe faltava. Na hora da fome tecia um lindo peixe, com cuidado de escamas. E eis que o peixe estava na mesa, pronto para ser comido. Se sede vinha, suave era a lã cor de leite que entremeava o tapete. E à noite, depois de lançar seu fio de escuridão, dormia tranquila.</p>
        <p>Tecer era tudo o que fazia. Tecer era tudo o que queria fazer.</p>
        <p>Mas tecendo e tecendo, ela própria trouxe o tempo em que se sentiu sozinha, e pela primeira vez pensou em como seria bom ter um marido ao lado.</p>
        <p>Não esperou o dia seguinte. Com capricho de quem tenta uma coisa nunca conhecida, começou a entremear no tapete as lãs e as cores que lhe dariam companhia. E aos poucos seu desejo foi aparecendo, chapéu emplumado, rosto barbado, corpo aprumado, sapato engraxado. Estava justamente acabando de entremear o último fio da ponta dos sapatos, quando bateram à porta.</p>
        <p>Nem precisou abrir. O moço meteu a mão na maçaneta, tirou o chapéu de pluma, e foi entrando em sua vida. Aquela noite, deitada no ombro dele, a moça pensou nos lindos filhos que teceria para aumentar ainda mais a sua felicidade.</p>
        <p>E feliz foi, durante algum tempo. Mas se o homem tinha pensado em filhos, logo os esqueceu. Porque tinha descoberto o poder do tear, em nada mais pensou a não ser nas coisas todas que ele poderia lhe dar.</p>
        <p>— Uma casa melhor é necessária — disse para a mulher. E parecia justo, agora que eram dois.</p>
        <p>Exigiu que escolhesse as mais belas lãs cor de tijolo, fios verdes para os batentes, e pressa para a casa acontecer.</p>
        <p>Mas pronta a casa, já não lhe pareceu suficiente.</p>
        <p>— Para que ter casa, se podemos ter palácio? — perguntou. Sem querer resposta imediatamente ordenou que fosse de pedra com arremates em prata.</p>
        <p>Dias e dias, semanas e meses trabalhou a moça tecendo tetos e portas, e pátios e escadas, e salas e poços. A neve caía lá fora, e ela não tinha tempo para chamar o sol. A noite chegava, e ela não tinha tempo para arrematar o dia. Tecia e entristecia, enquanto sem parar batiam os pentes acompanhando o ritmo da lançadeira.</p>
        <p>Afinal o palácio ficou pronto. E entre tantos cômodos, o marido escolheu para ela e seu tear o mais alto quarto da mais alta torre.</p>
        <p>— É para que ninguém saiba do tapete — ele disse. E antes de trancar a porta à chave, advertiu: — Faltam as estrebarias. E não se esqueça dos cavalos!</p>
        <p>Sem descanso tecia a mulher os caprichos do marido, enchendo o palácio de luxos, os cofres de moedas, as salas de criados. Tecer era tudo o que fazia. Tecer era tudo o que queria fazer.</p>
        <p>E tecendo, ela própria trouxe o tempo em que sua tristeza lhe pareceu maior que o palácio com todos os seus tesouros. E pela primeira vez pensou em como seria bom estar sozinha de novo.</p>
        <p>Só esperou anoitecer. Levantou-se enquanto o marido dormia sonhando com novas exigências. E descalça, para não fazer barulho, subiu a longa escada da torre, sentou-se ao tear.</p>
        <p>Desta vez não precisou escolher linha nenhuma. Segurou a lançadeira ao contrário, e jogando-a veloz de um lado para o outro, começou a desfazer seu tecido. Desteceu os cavalos, as carruagens, as estrebarias, os jardins. Depois desteceu os criados e o palácio e todas as maravilhas que continha. E novamente se viu na sua casa pequena e sorriu para o jardim além da janela.</p>
        <p>A noite acabava quando o marido, estranhando a cama dura, acordou e, espantado, olhou em volta. Não teve tempo de se levantar. Ela já desfazia o desenho escuro dos sapatos, e ele viu seus pés desaparecendo, sumindo as pernas. Rápido, o nada subiu-lhe pelo corpo, tomou o peito aprumado, o emplumado chapéu.</p>
        <p>Então, como se ouvisse a chegada do sol, a moça escolheu uma linha clara. E foi passando-a devagar entre os fios, delicado traço de luz, que a manhã repetiu na linha do horizonte.</p>
    </div>
</div>

<div class="trilha-links-secao">
    <div class="trilha-links-titulo">
        <i class="bi bi-collection-play-fill me-2"></i> Materiais de apoio e referências:
    </div>
    <div class="trilha-resource-cards-grid">
        <a href="/static/rede_miradas/documentos/slide_genero_conto.pdf" target="_blank" rel="noopener noreferrer" class="trilha-resource-card card-drive">
            <div class="resource-card-left">
                <div class="resource-card-icon icon-slide"><i class="bi bi-file-earmark-slides-fill"></i></div>
                <div class="resource-card-info">
                    <span class="resource-card-badge badge-slide">Apresentação</span>
                    <span class="resource-card-name">Slide: O Gênero Conto</span>
                    <span class="resource-card-domain">PDF / Slide da Trilha</span>
                </div>
            </div>
            <div class="resource-card-action">Visualizar <i class="bi bi-box-arrow-up-right"></i></div>
        </a>
        <a href="https://youtu.be/cGJ7pcgr0C8?si=BCA6m-JptqbpdKcD" target="_blank" rel="noopener noreferrer" class="trilha-resource-card card-youtube">
            <div class="resource-card-left">
                <div class="resource-card-icon icon-youtube"><i class="bi bi-youtube"></i></div>
                <div class="resource-card-info">
                    <span class="resource-card-badge badge-youtube">Vídeo Aula</span>
                    <span class="resource-card-name">Conto e Crônica: Diferenças</span>
                    <span class="resource-card-domain">youtube.com</span>
                </div>
            </div>
            <div class="resource-card-action">Assistir <i class="bi bi-box-arrow-up-right"></i></div>
        </a>
        <a href="https://youtu.be/IuNygaVSD-g?si=teGwfdSzDh5uuj4f" target="_blank" rel="noopener noreferrer" class="trilha-resource-card card-youtube">
            <div class="resource-card-left">
                <div class="resource-card-icon icon-youtube"><i class="bi bi-play-circle-fill"></i></div>
                <div class="resource-card-info">
                    <span class="resource-card-badge badge-youtube">Vídeo Complementar</span>
                    <span class="resource-card-name">Entendendo os Gêneros Narrativos</span>
                    <span class="resource-card-domain">youtube.com</span>
                </div>
            </div>
            <div class="resource-card-action">Assistir <i class="bi bi-box-arrow-up-right"></i></div>
        </a>
    </div>
</div>"""

                TopicoUnidadeTrilha.objects.create(
                    unidade=un1,
                    titulo='Conto e Crônica: como diferenciar?',
                    conteudo=conteudo_un1,
                    ordem=1,
                    ativo=True
                )

                # Unidade 2
                un2 = UnidadeTrilha.objects.create(
                    trilha=card,
                    numero=2,
                    titulo='Crônicas finalistas da Olimpíada Nacional de Língua Portuguesa',
                    ordem=2,
                    ativo=True
                )

                conteudo_un2 = """<p>A tradicional Olimpíada Nacional de Língua Portuguesa <em>Escrevendo o Futuro</em> movimentou estudantes do país inteiro até o ano de 2024, quando foi encerrada. Existiam categorias de acordo com os anos e níveis do ensino básico: poema, memórias literárias, crônica, artigo de opinião e videodocumentário.</p>
<p>O arquivo a seguir traz todos os textos finalistas da edição de 2019, que tinha como tema a frase <strong>"O lugar onde vivo"</strong>. Aproveite para ler as crônicas vencedoras!</p>

<div class="trilha-links-secao">
    <div class="trilha-links-titulo">
        <i class="bi bi-file-earmark-pdf-fill me-2"></i> Documento e Textos Finalistas:
    </div>
    <div class="trilha-resource-cards-grid">
        <a href="/static/rede_miradas/documentos/textos_finalistas_olimpiada_2019.pdf" target="_blank" rel="noopener noreferrer" class="trilha-resource-card card-pdf">
            <div class="resource-card-left">
                <div class="resource-card-icon icon-pdf"><i class="bi bi-file-earmark-pdf-fill"></i></div>
                <div class="resource-card-info">
                    <span class="resource-card-badge badge-pdf">PDF Completo</span>
                    <span class="resource-card-name">Textos Finalistas da Olimpíada 2019</span>
                    <span class="resource-card-domain">PDF da Trilha</span>
                </div>
            </div>
            <div class="resource-card-action">Baixar / Ler <i class="bi bi-box-arrow-up-right"></i></div>
        </a>
    </div>
</div>"""

                TopicoUnidadeTrilha.objects.create(
                    unidade=un2,
                    titulo='Olimpíada Nacional de Língua Portuguesa 2019',
                    conteudo=conteudo_un2,
                    ordem=1,
                    ativo=True
                )

                # Unidade 3
                un3 = UnidadeTrilha.objects.create(
                    trilha=card,
                    numero=3,
                    titulo='Lá na minha terra',
                    ordem=3,
                    ativo=True
                )

                conteudo_un3 = """<p>A crônica a seguir foi finalista da Olimpíada Nacional de Língua Portuguesa em 2019, cujo tema era <em>"O lugar onde vivo"</em>.</p>

<div class="trilha-leitura-box">
    <div class="trilha-leitura-header">
        <h4 class="trilha-leitura-title"><i class="bi bi-pen me-2"></i> Lá na minha terra</h4>
        <p class="trilha-leitura-autor">Por Açucena Martilho Diniz</p>
    </div>
    <div class="trilha-leitura-corpo">
        <p>Dizem que o bom filho a casa torna...</p>
        <p>E eu, depois de estudar e viver alguns anos longe, também voltei para a minha terra natal. E foi a partir dessa minha volta que me dei conta de uma particularidade dessa cidadezinha: que ninguém é livre, todo mundo é de alguém. Pode parecer estranho, eu sei, mas vou explicar.</p>
        <p>Aconteceu que, nos primeiros instantes de minha volta, ao desembarcar na rodoviária da cidade, olhos curiosos me acompanhavam. Eu, com duas malas e alguns anos adquiridos fora dali, despertei o interesse de quem por ali passava.</p>
        <p>— Quem será este que está chegando? – perguntavam as comadres.</p>
        <p>— Parece com o Marquinho.</p>
        <p>— Marquinho?</p>
        <p>— É, aquele, do João do bar.</p>
        <p>— Nada, tá mais para o Pedrinho, do Zé do posto.</p>
        <p>E assim as tentativas de adivinhações prosseguiram, e eu segui adiante.</p>
        <p>Mais tarde, precisando comprar algumas coisas, fui à venda do Português e, diante do caixa, uma criança dizia:</p>
        <p>— É para marcar!</p>
        <p>— Marcar para quem?</p>
        <p>— Marcar para a Maria!</p>
        <p>— Qual Maria?</p>
        <p>— É a Maria do João Riso.</p>
        <p>Agora estava explicado para quem era a pendura.</p>
        <p>Na volta para casa, passo pela Praça São Pedro que, como de costume, reúne muitos senhores a distraírem-se com jogos de baralho. Não se preocupam com o tempo e nem com a prosa entre eles, que é para quem quiser ouvir:</p>
        <p>— Ficou sabendo do que aconteceu com o Neco do João leiteiro?</p>
        <p>— Não, o que foi?</p>
        <p>— Deu praga na roça dele, perdeu tudo o que tinha plantado.</p>
        <p>— Coitado! Será que deu também na plantação do Tonho, do Dito Saracura? É vizinho dele lá no sítio.</p>
        <p>— Ah, esse eu não sei...</p>
        <p>E eu vou passando e, além de saber das novidades, percebo mais uma vez que por aqui não adianta falar só o nome, tem que dizer de quem é, senão ninguém vai saber.</p>
        <p>No cair da tarde, o sino da Igreja Matriz toca, é para anunciar o falecimento de um ente querido que ali morava. Todos saem para fora de suas casas para ouvir direito de quem se trata, e a notícia vem:</p>
        <p>— Faleceu hoje José Nascimento dos Santos.</p>
        <p>Quem é? Ninguém sabe! E é por isso que o comunicado vem completo:</p>
        <p>— Faleceu hoje José Nascimento dos Santos, o "Zé da Lurde". Agora sim, todos sabem de quem foi o infeliz dia.</p>
        <p>E assim chego a uma conclusão sobre essa cidadezinha: ela tem um povo muito bom e hospitaleiro, uma terra vermelha da boa, lindas paisagens verdes... E o diferencial é que nesse lugar ninguém está sozinho, todo mundo é de alguém. Se quer ser conhecido por aqui tenha sempre alguém a quem pertencer, conselho de amigo, fica mais fácil. Mas e eu? A quem eu pertenço? Quem pertence a mim? Ahhh, eu sou filho de Riversul, e vou logo tratar de arranjar alguém pra chamar de meu.</p>
    </div>
    <div class="trilha-leitura-rodape">
        Professora Orientadora: Fernanda Aparecida Mendes de Freitas<br>
        EE Lázaro Soares Professor, Riversul-SP
    </div>
</div>"""

                TopicoUnidadeTrilha.objects.create(
                    unidade=un3,
                    titulo='Crônica: Lá na minha terra',
                    conteudo=conteudo_un3,
                    ordem=1,
                    ativo=True
                )

                # Unidade 4
                un4 = UnidadeTrilha.objects.create(
                    trilha=card,
                    numero=4,
                    titulo='Quebra-molas',
                    ordem=4,
                    ativo=True
                )

                conteudo_un4 = """<p>A crônica a seguir foi escrita por Raíssa Julião, aluna do campus IFRN São Paulo do Potengi. O texto participou da prova de crônicas da Semadec 2024.</p>

<div class="trilha-leitura-box">
    <div class="trilha-leitura-header">
        <h4 class="trilha-leitura-title"><i class="bi bi-pen me-2"></i> Quebra-molas</h4>
        <p class="trilha-leitura-autor">Por Raissa Josefa Julião Bezerra</p>
    </div>
    <div class="trilha-leitura-corpo">
        <p>As duas crianças voltavam da escola, felizes, seus uniformes manchados de tinta guache e danone. Traziam na cabeça tiaras com longas orelhas de cartolina, a ponta do nariz e bochechas pintadas de coelhinho, como toda "tia" faz em época de páscoa. Riam alegres, segurando seus pequenos ovos de chocolate, as mãos quentes derretendo a sobremesa que a mãe deixaria comer só após o jantar. Naquele dia, provavelmente, o maior conflito enfrentado pelos pequenos foi escolher a cor do giz de cera ideal para pintar a tarefa de classe.</p>
        <p>Toda cena durou um segundo enquanto eu observava de dentro do velho ônibus no qual eu voltava para casa todos os dias, depois de uma jornada cansativa no IFRN. Suada, com fome, indisposta e sobrecarregada, ouvindo uma senhora tagarelando sobre seu filho para a moça ao lado... Era um fim de tarde, daqueles em que tudo que você quer é chegar em casa e dormir até recuperar suas energias, esquecer das brigas entre colegas e das obrigações que surgem como formigas atrás de um doce qualquer.</p>
        <p>Sem dúvidas, eu preferia estar no lugar daquelas crianças. Vê-las me fez sentir saudade do meu tempo de infância quando, em dias de sexta-feira como hoje, eu voltava mais feliz da escola, pois sabia que meu pai faria churrasco no fim de semana. Tempos como esse não voltam mais... Tudo é mais fácil quando se é criança: sem trabalhos, sem atividades pendentes, provas, relacionamentos nem outras mil coisas com que se preocupar. Afinal, ir para a escola se tornou diferente ao entrar no ensino médio. Desde então, é normal andar com olheiras pelos corredores, ter poucas horas de sono e conviver com casais de namorados às sete da manhã agarrados por aí (ninguém aguenta). Suspirei fundo, completamente vencida pela minha realidade e pelo meu cansaço... De repente, um solavanco me sacudiu, derrubando a mochila que já queria cair pelos ombros faz tempo: era um quebra-molas daqueles que o motorista não vê e o passageiro não espera. Em meio a objetos e pessoas sacudidas, abaixei para recolher a mochila e a cartolina verde do trabalho, que por sorte não amassou antes do seminário.</p>
        <p>Pensando bem... Até que todo o cansaço vale a pena quando, após um contraturno de várias atividades escolares, eu e meus amigos sentamos nas escadas em frente à guarita, compartilhando risadas, fofocas e açaí repleto de leite condensado. É engraçado pensar que, se estudar no IF não estivesse no meu destino, fins de tarde como esses não teriam o mesmo significado: talvez eu perdesse meu tempo num jogo qualquer no notebook.</p>
        <p>Certamente, o esgotamento físico e emocional fazem com que eu esqueça, às vezes, como também é divertido estudar na instituição. Sabe como é pular de alegria ao conseguir um concreto razoável na aula de materiais? Sabe como é ensaiar uma peça por semanas e, no dia da apresentação, ver o auditório ir à loucura? Coisas assim me fazem sentir como uma criança no recreio da escolinha... No fim das contas, minha trajetória aqui no IF não é sempre flores, mas me traz momentos felizes assim como quando eu era pequena. Cada dia é um capítulo na história da minha adolescência e meu tão esperado futuro brilhante vai ganhando forma com conhecimento, sabedoria (às vezes) e mais algumas coisinhas...</p>
        <p>Foi quando eu percebi que o ônibus chegou ao destino: uma rodoviária repleta de velhinhos, mototáxis e cadeiras de bar na calçada. Geralmente nesse ponto da viagem minha sensação é de cansaço e estresse, mas dessa vez eu sentia como se, ao chegar em casa, chocolates me esperassem. O cheiro e a fumaça do churrasquinho me lembravam os almoços de fim de semana com meu pai, então resolvi, pela primeira vez em muito tempo, comprar um espetinho após esse longo dia de aula.</p>
        <p>Definitivamente, alguma coisa mudou naquele percurso diário: ali estava uma Raissa feliz, voltando para casa com suas orelhinhas de cartolina imaginária.</p>
    </div>
</div>"""

                TopicoUnidadeTrilha.objects.create(
                    unidade=un4,
                    titulo='Crônica: Quebra-molas',
                    conteudo=conteudo_un4,
                    ordem=1,
                    ativo=True
                )

                # Unidade 5
                un5 = UnidadeTrilha.objects.create(
                    trilha=card,
                    numero=5,
                    titulo='A perca',
                    ordem=5,
                    ativo=True
                )

                conteudo_un5 = """<p>Uma das maiores cronistas brasileiras da atualidade, Martha Medeiros é a autora de <em>"A perca"</em>. Aproveite a leitura!</p>

<div class="trilha-leitura-box">
    <div class="trilha-leitura-header">
        <h4 class="trilha-leitura-title"><i class="bi bi-pen me-2"></i> A perca</h4>
        <p class="trilha-leitura-autor">Por Martha Medeiros</p>
    </div>
    <div class="trilha-leitura-corpo">
        <p>Da série “só acontece comigo”: estava parada num sinal da Avenida Ipiranga quando um carro encostou ao lado do meu. A motorista abriu a janela e pediu para eu abrir a minha. Era uma moça simpática que me perguntou: “Martha, o certo é dizer perda ou perca?”.</p>
        <p>“Hãn?”</p>
        <p>“É perda de tempo ou perca de tempo? Como se diz?”</p>
        <p>A pergunta era tão inusitada para a hora e o local, tão surpreendente, vinda de alguém que eu não conhecia, que me deu um branco: por um milésimo de segundo eu não soube o que responder. Perca de tempo, isso existe? Então o sinal abriu, os carros da frente começaram a engatar a primeira, eu olhei para ela e disse: “É perda de tempo”.</p>
        <p>Ela sorriu em agradecimento e foi em frente. Meu carro ainda ficou um tempo parado. Eu parada no tempo. Perca de tempo.</p>
        <p>Dei uma risada e segui meu rumo também.</p>
        <p>Se alguém te diz “não perca tempo”, e todos te dizem isso o tempo todo, como não confundir? Tantos confundem. São coagidos a tal. E, cá entre nós, a “perca” parece mais amena do que a perda.</p>
        <p>A perca de um amor é quase tão corriqueira como a perca do capítulo da novela. A perca é feira livre. A perca é festiva. A perca é música popular.</p>
        <p>Já a perda é sinfonia de Beethoven.</p>
        <p>A perca acontece no verão. A perca de uma cadeirinha de praia, a perca de um palito premiado de picolé.</p>
        <p>As perdas acontecem no inverno.</p>
        <p>A perca é simplória, a perca é distraída, a perca é provisória, logo, logo reencontrarão o que está faltando.</p>
        <p>A perda é para sempre.</p>
        <p>As percas reinventam o vocabulário e seu sentido, não são graves, as percas são imperfeições perdoáveis, as percas são inocentes.</p>
        <p>As perdas são catastróficas, nada têm de folclóricas.</p>
        <p>A perca é um erro gramatical, e apenas esse erro ela contém. De resto, não faz mal a ninguém.</p>
        <p>A perda é um acerto gramatical, mas só esse acerto ela contém. De resto, é brutal.</p>
        <p>Se eu pudesse voltar no tempo, reconstituiria a cena de outra forma:</p>
        <p>“Martha, é perda de tempo ou perca de tempo? Como é que se diz?”</p>
        <p>“O correto é dizer perda, mas é muito solene. Perca dói menos por ser mais trivial”.</p>
    </div>
</div>"""

                TopicoUnidadeTrilha.objects.create(
                    unidade=un5,
                    titulo='Crônica: A perca',
                    conteudo=conteudo_un5,
                    ordem=1,
                    ativo=True
                )

                # Unidade 6
                un6 = UnidadeTrilha.objects.create(
                    trilha=card,
                    numero=6,
                    titulo='Crônicas de Paris',
                    ordem=6,
                    ativo=True
                )

                conteudo_un6 = """<p>Mais uma crônica em vídeo para o acervo. Nas edições do <em>Jornal Hoje</em>, na Globo, é muito comum que os jornalistas correspondentes da emissora em várias partes do mundo produzam crônicas de viagem. No YouTube é possível encontrar vídeos de Nova York, Jerusalém, Lisboa, Tóquio ou, no caso a seguir, em Paris.</p>
<p>Assista à videocrônica a respeito do verão na Cidade Luz e compare com uma notícia qualquer de um jornal televisivo. Em que elas são diferentes?</p>

<div class="trilha-links-secao">
    <div class="trilha-links-titulo">
        <i class="bi bi-play-btn-fill me-2"></i> Assista à videocrônica:
    </div>
    <div class="trilha-resource-cards-grid">
        <a href="https://youtu.be/6NW2-BuQ2pQ?si=t-GdDPIN-PkHleIL" target="_blank" rel="noopener noreferrer" class="trilha-resource-card card-youtube">
            <div class="resource-card-left">
                <div class="resource-card-icon icon-youtube"><i class="bi bi-youtube"></i></div>
                <div class="resource-card-info">
                    <span class="resource-card-badge badge-youtube">Videocrônica</span>
                    <span class="resource-card-name">Crônicas de Paris (Jornal Hoje / Globo)</span>
                    <span class="resource-card-domain">youtube.com</span>
                </div>
            </div>
            <div class="resource-card-action">Assistir no YouTube <i class="bi bi-box-arrow-up-right"></i></div>
        </a>
    </div>
</div>"""

                TopicoUnidadeTrilha.objects.create(
                    unidade=un6,
                    titulo='Videocrônica: Crônicas de Paris',
                    conteudo=conteudo_un6,
                    ordem=1,
                    ativo=True
                )

                # Unidade 7
                un7 = UnidadeTrilha.objects.create(
                    trilha=card,
                    numero=7,
                    titulo='Isso é ser brasileiro!',
                    ordem=7,
                    ativo=True
                )

                conteudo_un7 = """<p>As crônicas fazem parte do dia a dia do jornalismo e você assiste a muitas, mesmo sem perceber. A seguir, veja uma crônica esportiva de Fernanda Gentil refletindo a partir de acontecimentos das Olimpíadas.</p>

<div class="trilha-links-secao">
    <div class="trilha-links-titulo">
        <i class="bi bi-play-btn-fill me-2"></i> Assista à videocrônica:
    </div>
    <div class="trilha-resource-cards-grid">
        <a href="https://youtu.be/R2SuZEA6vik?si=O_lhh1g9Qkec8zAk" target="_blank" rel="noopener noreferrer" class="trilha-resource-card card-youtube">
            <div class="resource-card-left">
                <div class="resource-card-icon icon-youtube"><i class="bi bi-youtube"></i></div>
                <div class="resource-card-info">
                    <span class="resource-card-badge badge-youtube">Crônica Esportiva</span>
                    <span class="resource-card-name">Isso é ser brasileiro! — Fernanda Gentil</span>
                    <span class="resource-card-domain">youtube.com</span>
                </div>
            </div>
            <div class="resource-card-action">Assistir no YouTube <i class="bi bi-box-arrow-up-right"></i></div>
        </a>
    </div>
</div>"""

                TopicoUnidadeTrilha.objects.create(
                    unidade=un7,
                    titulo='Videocrônica: Isso é ser brasileiro!',
                    conteudo=conteudo_un7,
                    ordem=1,
                    ativo=True
                )

                # Unidade 8
                un8 = UnidadeTrilha.objects.create(
                    trilha=card,
                    numero=8,
                    titulo='Varal de Sonhos',
                    ordem=8,
                    ativo=True
                )

                conteudo_un8 = """<p>A crônica a seguir foi escrita pela estudante do IFRN Ozilane Chagas, na época aluna do curso técnico de Informática no campus João Câmara. O texto foi produzido para uma prova de crônicas dentro da Semadec do IFRN-JC no ano de 2019 e obteve o primeiro lugar.</p>

<div class="trilha-leitura-box">
    <div class="trilha-leitura-header">
        <h4 class="trilha-leitura-title"><i class="bi bi-pen me-2"></i> Varal de sonhos</h4>
        <p class="trilha-leitura-autor">Por Ozilane Chagas (coautoria: Julianny Simião)</p>
    </div>
    <div class="trilha-leitura-corpo">
        <p>Há certa leveza nessas tardes de domingo. Acima do Torreão, os tons alaranjados do pôr-do-sol iluminam as crianças brincando entre folhas secas; as senhoras comentando sobre as vidas da cidade; a mãe com os olhos marejados observando os primeiros passos do bebê. Seu Geovan consertando o som do carro... E eu observando esse curta-metragem através da minha janela. Cada um sendo feliz ao seu modo, sem pressa alguma, como se o caos do mundo por esse momento cessasse, dando lugar ao sossego.</p>
        <p>Esses tons de fim de tarde iluminam também as minhas roupas no varal. A minha farda branca e verde tremulando ao vento, já quase seca e aguardando a manhã seguinte. Naquele mesmo momento, muitas fardas semelhantes secam em tantos varais do Mato Grande. Serão retiradas ainda hoje ou amanhã, antes do sol nascer. Acompanharão cada aluno até a mesma escola, que é também nossa casa e casa de tanta gente há dez anos: o Instituto Federal de Educação, Ciência e Tecnologia do Rio Grande do Norte, na cidade de João Câmara. Um nome bem grande que a gente chama apenas de iéfe.</p>
        <p>Minha peça de roupa preferida, quase íntima, companheira de anos inesquecíveis. Será que consigo falar do lugar para onde a levo quase todo dia? Descrever o indescritível que é o IFRN para mim? Posso tentar dizendo que cada detalhe de lá me encanta: o verdinho das árvores, os alunos nos banquinhos do xadrez, a biblioteca repleta de livros a descobrir ou mesmo a paz no campo de futebol vazio...</p>
        <p>Porém, como costumo dizer, o que faz essa escola tão linda são as pessoas que tenho a oportunidade de conhecer. Muitas delas estarão sempre tatuadas em meu coração, como Francine, a secretária acadêmica que em uma simples conversa me ensinou a importância de colecionar sorrisos e momentos felizes, pois onde há alegria, há realização pessoal. Não esqueço também o porteiro Tarcísio e o singelo "bom dia" de toda manhã; o professor que ensina a matéria que mais amo; o carinho das pedagogas; as gargalhadas cheias de alegria dos amigos de alma que conquistei... E, claro: as histórias sem graça do professor Nickerson — que contadas por ele parecem ser a coisa mais engraçada do mundo!</p>
        <p>Vez ou outra, antes de entregar o bolo e o suco do lanche, Tia Lu me abraça e diz que sou uma florzinha desabrochando. Acho que ela soube mesmo, com toda essa ternura, definir o que aconteceu comigo! Olhando para trás, vejo que venho germinando desde o primeiro dia de aula, quando pisei na recepção sentindo frio na barriga e o receio do desconhecido.</p>
        <p>E isso não acontece só comigo: histórias de superação vejo por toda parte. É surreal perceber que adolescentes como eu, por meio da educação, desenvolvem seus talentos, descobrem novos hobbies, novos horizontes... Mesmo vindo de famílias carentes e de gerações anteriores que não tiveram oportunidades, esses jovens vão rompendo ciclos e inaugurando outras épocas. Com tudo isso, realidades são transformadas e a região germina junto. O crescimento é coletivo e transcende pelas mais diferentes áreas: ver tudo isso diante dos meus olhos me faz acreditar em um mundo melhor.</p>
        <p>Agora o sol já se pôs. As estrelas me convidam também a imaginar minha própria trajetória daqui pra frente. Depois de quatro anos de luta e aprendizado, vividos com muita gratidão, penso no quão difícil será, em breve, dar adeus à escola que foi palco do meu crescimento, de momentos felizes e tristes; aventuras e desventuras; florescimento. Pelo que já vivi, sei que posso ir além do que imagino. Voarei sem medo rumo aos meus sonhos, porém na certeza de retornar à minha João Câmara, a essa mesma paisagem de fim de tarde. Espero que os conhecimentos que irei construir até lá possam fazer daqui um lugar ainda melhor...</p>
        <p>De dentro da cozinha, minha mãe me chama pra jantar. Vejo novamente o varal: a umidade da camisa vai se despedindo com a chegada da noite. Meus olhos também estão estendidos, mas vão demorar a secar.</p>
    </div>
</div>"""

                TopicoUnidadeTrilha.objects.create(
                    unidade=un8,
                    titulo='Crônica: Varal de Sonhos',
                    conteudo=conteudo_un8,
                    ordem=1,
                    ativo=True
                )

        self.stdout.write(self.style.SUCCESS('Trilhas, subtópicos, unidades e tópicos cadastrados com sucesso!'))

