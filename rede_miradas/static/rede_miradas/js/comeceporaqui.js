/* =====================================================
   PÁGINA "COMECE POR AQUI" — scripts
   ===================================================== */


/* ---------- Destaques: troca de banners (só se houver mais de 1) ---------- */

let slideAtual = 0;
let timerSlides = null;

const slides = document.querySelectorAll('.slide');


function mostrarSlide(indice) {

    if (slides.length === 0) {
        return;
    }

    slides[slideAtual].classList.remove('ativo');

    slideAtual = (indice + slides.length) % slides.length;

    slides[slideAtual].classList.add('ativo');
}


function iniciarTimer() {

    if (slides.length < 2) {
        return;
    }

    clearInterval(timerSlides);

    timerSlides = setInterval(function () {
        mostrarSlide(slideAtual + 1);
    }, 5000);
}


/* usado pelos botões ❮ ❯ dos destaques */
function mudarSlide(direcao) {

    mostrarSlide(slideAtual + direcao);

    iniciarTimer();
}

iniciarTimer();


/* ---------- Animações ao rolar a página ---------- */

/*
   Esconde o elemento e, quando ele aparece na tela, adiciona a classe
   "visivel" (o CSS faz a animação). Ao sair da tela, reseta para
   animar de novo na volta.
*/
/*
   Esconde o elemento e, quando ele aparece na tela, adiciona a classe
   "visivel" (o CSS faz a animação). Acontece UMA vez só: depois de
   animar, o elemento fica visível e não anima de novo ao rolar.
*/
function animarAoRolar(elemento, margemInferior) {

    if (!elemento || !('IntersectionObserver' in window)) {
        return;
    }

    /* anima quando o elemento já entrou X% da altura da tela (padrão: 12%) */
    const margem = margemInferior === undefined ? 12 : margemInferior;

    /* 1) esconde e força o navegador a registrar esse estado */
    elemento.classList.add('anim-pronto');
    void elemento.offsetWidth;

    /* 2) mostra com animação na primeira vez que aparecer */
    const observador = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (entrada) {
            if (entrada.isIntersecting) {
                elemento.classList.add('visivel');
                observador.disconnect();   /* nunca mais anima */
            }
        });
    }, { rootMargin: '0px 0px -' + margem + '% 0px', threshold: 0 });

    observador.observe(elemento);
}
/* ---- COMPUTADOR: animações de cada parte da seção ---- */
/* (no celular elas não rodam: lá cada seção inteira aparece, veja mais abaixo) */

const ehCelular = window.matchMedia('(max-width: 767.98px)').matches;

if (!ehCelular) {

    /* Aprenda. Crie. Conecte.: círculo, depois título + texto */
    animarAoRolar(document.querySelector('.aprenda-texto'));

    /* Trilhas: título + texto */
    animarAoRolar(document.querySelector('.trilhas-cabecalho'));

    /* Trilhas: ícones entram pelas laterais */
    animarAoRolar(document.querySelector('.trilhas'));

    /* Júri Popular: estrelas entram uma de cada lado */
    animarAoRolar(document.querySelector('.juri'));
}


/* ---- CELULAR: cada seção aparece suavemente ao rolar a página ---- */

(function () {

    if (!ehCelular || !('IntersectionObserver' in window)) {
        return;
    }

    const secoes = document.querySelectorAll(
        '.aprenda, .painel-curtas, .trilhas, .painel-selos, .juri, .painel-noticias, .secao-final .container'
    );

    const observadorSecoes = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (entrada) {
            if (entrada.isIntersecting) {
                entrada.target.classList.add('revelado');
                observadorSecoes.unobserve(entrada.target);   /* anima uma vez só */
            }
        });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    secoes.forEach(function (secao) {
        secao.classList.add('revelar');
        observadorSecoes.observe(secao);
    });

})();


/* ---------- Cards do Aprenda no celular: um por vez, troca a cada 3s ---------- */

(function () {

    const blocoCards = document.querySelector('.cards-bloco');

    if (!blocoCards) {
        return;
    }

    const cards = blocoCards.querySelectorAll('.card-bloco');
    const telaCelular = window.matchMedia('(max-width: 767.98px)');

    let cardAtual = 0;
    let timerCards = null;

    function mostrarCard(indice) {
        cards.forEach(function (card, posicao) {
            card.classList.toggle('card-ativo', posicao === indice);
        });
    }

    function iniciarCards() {

        blocoCards.classList.add('cards-rotativo');

        cardAtual = 0;
        mostrarCard(cardAtual);

        clearInterval(timerCards);

        if (cards.length > 1) {
            timerCards = setInterval(function () {
                cardAtual = (cardAtual + 1) % cards.length;
                mostrarCard(cardAtual);
            }, 3000);   /* 3000 = 3 segundos */
        }
    }

    function pararCards() {

        clearInterval(timerCards);
        timerCards = null;

        blocoCards.classList.remove('cards-rotativo');

        cards.forEach(function (card) {
            card.classList.remove('card-ativo');
        });
    }

    function verificarTela() {
        if (telaCelular.matches) {
            iniciarCards();
        } else {
            pararCards();
        }
    }

    verificarTela();

    if (telaCelular.addEventListener) {
        telaCelular.addEventListener('change', verificarTela);
    } else {
        telaCelular.addListener(verificarTela);
    }

})();


/* ---------- Curtas em destaque: setas rolam a lista ---------- */

const viewportCurtas = document.querySelector('.curtas-viewport');


/* usado pelos botões ❮ ❯ das curtas */
function mudarCurta(direcao) {

    if (!viewportCurtas) {
        return;
    }

    const fim = viewportCurtas.scrollWidth - viewportCurtas.clientWidth - 4;

    /* se todas as curtas já cabem na tela, não há o que rolar */
    if (fim <= 0) {
        return;
    }

    /* chegou no fim e clicou em ❯ -> volta ao começo (e vice-versa) */
    if (direcao > 0 && viewportCurtas.scrollLeft >= fim) {
        viewportCurtas.scrollTo({ left: 0, behavior: 'smooth' });
        return;
    }

    if (direcao < 0 && viewportCurtas.scrollLeft <= 4) {
        viewportCurtas.scrollTo({ left: fim, behavior: 'smooth' });
        return;
    }

    /* computador: anda quase uma tela; celular: anda exatamente 3 curtas */
    let passo = viewportCurtas.clientWidth * 0.85;

    if (window.matchMedia('(max-width: 767.98px)').matches) {

        const curta = viewportCurtas.querySelector('.curta-card');
        const lista = viewportCurtas.querySelector('.curtas-lista');

        if (curta && lista) {
            const espaco = parseFloat(getComputedStyle(lista).columnGap) || 0;
            passo = (curta.offsetWidth + espaco) * 3;
        }
    }

    viewportCurtas.scrollBy({
        left: passo * direcao,
        behavior: 'smooth'
    });
}


/* ---------- Botões: animação igual à do botão de login ---------- */

(function () {

    const botoesAnimados = document.querySelectorAll(
        '.btn-pilula, .btn-amarelo, .slide-fixo-botao, .secao-final .btn-neon'
    );

    botoesAnimados.forEach(function (botao) {

        botao.addEventListener('click', function (evento) {

            const destino = botao.getAttribute('href');

            /* sem link, nova aba ou Ctrl/Shift + clique: deixa o navegador agir normal */
            if (!destino || botao.target === '_blank' || evento.button !== 0 ||
                evento.ctrlKey || evento.metaKey || evento.shiftKey) {
                return;
            }

            evento.preventDefault();

            /* já está animando: ignora o segundo clique */
            if (botao.classList.contains('animando')) {
                return;
            }

            /* começa a animação (a camada branca abre do centro) */
            botao.classList.add('animando');

            /* espera a animação terminar e abre a página */
            setTimeout(function () {
                window.location.href = botao.href;
            }, 450);
        });
    });

    /* se o usuário voltar pelo botão "voltar" do navegador, o botão volta ao normal */
    window.addEventListener('pageshow', function () {
        botoesAnimados.forEach(function (botao) {
            botao.classList.remove('animando');
        });
    });

})();


/* ---------- Seção final: triângulos passam por cima do rodapé ---------- */

function ajustarTriangulosFinal() {

    const secaoFinal = document.querySelector('.secao-final');
    const footer = document.querySelector('footer');
    const clip = document.querySelector('.triangulos-final-clip');
    const wrapperTriangulos = document.querySelector('.triangulos-final');

    if (!secaoFinal || !footer || !clip || !wrapperTriangulos) {
        return;
    }

    clip.style.height = `${secaoFinal.offsetHeight + footer.offsetHeight}px`;
    wrapperTriangulos.style.height = `${secaoFinal.offsetHeight}px`;
}

window.addEventListener('load', ajustarTriangulosFinal);
window.addEventListener('resize', ajustarTriangulosFinal);