document.addEventListener("DOMContentLoaded", () => {
    const notificacoes = document.querySelectorAll(".notificacao");

    // Remove as notificações automaticamente após 5 segundos
    notificacoes.forEach((notificacao) => {
        setTimeout(() => {
            notificacao.classList.add("fade-out");
            setTimeout(() => notificacao.remove(), 500);
        }, 5000);
    });
});

// Estilos para animações de fade out 
document.head.insertAdjacentHTML("beforeend", `
<style>
.fade-out {
    opacity: 0;
    transition: opacity 0.5s ease-out;
}
</style>
`);
