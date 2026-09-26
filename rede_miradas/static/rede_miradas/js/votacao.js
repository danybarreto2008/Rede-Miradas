document.addEventListener('DOMContentLoaded', () => {

    const modal = document.getElementById('modalConfirmarVoto');

    if (!modal) {
        return;
    }

    modal.addEventListener('show.bs.modal', (evento) => {

        const botao = evento.relatedTarget;

        const curtaId = botao.getAttribute('data-curta-id');
        const curtaNome = botao.getAttribute('data-curta-nome');

        document.getElementById('inputCurtaId').value = curtaId;
        document.getElementById('nomeCurtaModal').textContent = curtaNome;
    });
});