/* =====================================================
   PÁGINA "COMO TUDO COMEÇOU" — scripts
   Mesmas animações da home: aparecer ao rolar (uma vez só)
   e botão com a camada branca abrindo do centro.
   ===================================================== */


/* ---------- Animações ao rolar a página ---------- */

/*
   Esconde o elemento (classe "anim-pronto") e, quando ele aparece na
   tela, adiciona "visivel" (o CSS faz a animação). Acontece UMA vez só.
*/
function animarAoRolar(elemento, margemInferior) {

    if (!elemento || !('IntersectionObserver' in window)) {
        return;
    }

    /* anima quando o elemento já entrou X% da altura da tela */
    const margem = margemInferior === undefined ? 8 : margemInferior;

    /* 1) esconde e força o navegador a registrar esse estado */
    elemento.classList.add('anim-pronto');
    void elemento.offsetWidth;

    /* 2) mostra com animação na primeira vez que aparecer */
    const observador = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (entrada) {

            /* também revela se a pessoa já passou direto por ele (ex.: recarregou no meio da página) */
            const jaPassou = entrada.boundingClientRect.top < 0;

            if (entrada.isIntersecting || jaPassou) {
                elemento.classList.add('visivel');
                observador.disconnect();
            }
        });
    }, { rootMargin: '0px 0px -' + margem + '% 0px', threshold: 0 });

    observador.observe(elemento);
}


/* blocos que sobem suavemente */
document.querySelectorAll('.pagina-sobre .revelar').forEach(function (elemento) {
    animarAoRolar(elemento, 8);
});

/* seções com estrelas que entram pelas laterais */
document.querySelectorAll('.pagina-sobre .sobre-anim').forEach(function (elemento) {
    animarAoRolar(elemento, 12);
});


/* ---------- Botões: animação igual à do botão de login ---------- */

(function () {

    const botoesAnimados = document.querySelectorAll('.pagina-sobre .btn-pilula');

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