/* Controla o carrossel */
let slideAtual = 0;

const slides = document.querySelectorAll('.slide');


/* Mostra o slide escolhido */
function mostrarSlide(indice) {

    if (slides.length === 0) {
        return;
    }


    /* Remove o slide atual */
    slides[slideAtual].classList.remove('ativo');


    /* Calcula o próximo slide */
    slideAtual = (indice + slides.length) % slides.length;


    /* Mostra o novo slide */
    slides[slideAtual].classList.add('ativo');
}


/* Botões de próximo e anterior */
function mudarSlide(direcao) {

    mostrarSlide(slideAtual + direcao);

    reiniciarTimer();
}


/* Faz o slide passar sozinho */
let timer = setInterval(() => {

    mostrarSlide(slideAtual + 1);

}, 5000);


/* Reinicia o temporizador */
function reiniciarTimer() {

    clearInterval(timer);

    timer = setInterval(() => {

        mostrarSlide(slideAtual + 1);

    }, 5000);
}

// Rola a lista de curtas para os lados ao clicar nas setas
function mudarCurta(direcao) {

    const lista = document.getElementById('curtasLista');

    if (!lista) return;

    const item = lista.querySelector('.curta-item');

    const distancia = item ? item.getBoundingClientRect().width + 20 : 200;

    lista.scrollBy({
        left: distancia * direcao,
        behavior: 'smooth'
    });

}

// ==========================================
// CARROSSEL DOS CURTAS
// ==========================================

let curtaPagina = 0;

const viewportCurtas = document.querySelector('.curtas-viewport');
const listaCurtas = document.querySelector('.curtas-lista');
const cardsCurtas = document.querySelectorAll('.curta-card');


function quantidadeCurtasVisiveis() {

    return 5;
}


function totalPaginasCurtas() {

    return Math.ceil(cardsCurtas.length / quantidadeCurtasVisiveis());
}


function atualizarCurtas() {

    if (!listaCurtas || cardsCurtas.length === 0) {
        return;
    }

    const quantidadeVisivel = quantidadeCurtasVisiveis();

    const totalPaginas = Math.ceil(cardsCurtas.length / quantidadeVisivel);

    if (curtaPagina >= totalPaginas) {
        curtaPagina = totalPaginas - 1;
    }

    if (curtaPagina < 0) {
        curtaPagina = 0;
    }

    const larguraCard = cardsCurtas[0].getBoundingClientRect().width;

    const estiloLista = window.getComputedStyle(listaCurtas);

    const gap = parseFloat(estiloLista.columnGap || estiloLista.gap) || 0;

    const deslocamentoPagina = (larguraCard + gap) * quantidadeVisivel;

    listaCurtas.style.transform = `translateX(-${curtaPagina * deslocamentoPagina}px)`;
}


function mudarCurta(direcao) {

    if (!listaCurtas || cardsCurtas.length === 0) {
        return;
    }

    const quantidadeVisivel = quantidadeCurtasVisiveis();

    const totalPaginas = Math.ceil(cardsCurtas.length / quantidadeVisivel);

    curtaPagina += direcao;

    if (curtaPagina >= totalPaginas) {
        curtaPagina = 0;
    }

    if (curtaPagina < 0) {
        curtaPagina = totalPaginas - 1;
    }

    atualizarCurtas();
}

// ==========================================
// AJUSTA O TEXTO DOS CARDS "APRENDA. CRIE. CONECTE."
// PARA SEMPRE CABER DENTRO DO CARD
// ==========================================

function ajustarTextoBlocos() {

    document.querySelectorAll('.card-bloco').forEach((card) => {

        const inner = card.querySelector('.card-bloco-inner');
        const texto = card.querySelector('.card-bloco-texto');

        if (!inner || !texto) {
            return;
        }

        let tamanho = 16;

        texto.style.fontSize = tamanho + 'px';

        while (inner.scrollHeight > inner.clientHeight && tamanho > 5) {

            tamanho -= 1;

            texto.style.fontSize = tamanho + 'px';
        }
    });
}


window.addEventListener('load', ajustarTextoBlocos);
window.addEventListener('resize', ajustarTextoBlocos);

function ajustarTriangulosFinal() {

    const secaoFinal = document.querySelector('.secao-final');
    const footer = document.querySelector('footer');
    const clip = document.querySelector('.triangulos-final-clip');
    const wrapperTriangulos = document.querySelector('.triangulos-final');

    if (!secaoFinal || !footer || !clip || !wrapperTriangulos) {
        return;
    }

    const alturaSecao = secaoFinal.offsetHeight;
    const alturaFooter = footer.offsetHeight;

    clip.style.height = `${alturaSecao + alturaFooter}px`;
    wrapperTriangulos.style.height = `${alturaSecao}px`;
}

window.addEventListener('load', ajustarTriangulosFinal);
window.addEventListener('resize', ajustarTriangulosFinal);