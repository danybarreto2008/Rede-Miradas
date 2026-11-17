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
/* Aprenda. Crie. Conecte.: círculo, depois título + texto */
animarAoRolar(document.querySelector('.aprenda-texto'));

/* Trilhas: título + texto */
animarAoRolar(document.querySelector('.trilhas-cabecalho'));

/* Trilhas: ícones entram pelas laterais */
animarAoRolar(document.querySelector('.trilhas'));

/* Júri Popular: estrelas entram uma de cada lado */
animarAoRolar(document.querySelector('.juri'));

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

    viewportCurtas.scrollBy({
        left: viewportCurtas.clientWidth * 0.85 * direcao,
        behavior: 'smooth'
    });
}


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