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