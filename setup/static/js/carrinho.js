document.addEventListener("DOMContentLoaded", () => {
    atualizarTotal();
});

function atualizarTotal() {
    fetch("/carrinho/detalhes/")
        .then(response => response.json())
        .then(data => {
            const totalElemento = document.getElementById("carrinho-total");
            if (totalElemento) {
                totalElemento.textContent = `R$${data.total.toFixed(2)}`;
            }

            const quantidadeElementos = document.querySelectorAll(".ingressos-qtd-1");
            quantidadeElementos.forEach(elemento => {
                const ingressoId = elemento.dataset.ingressoId;
                const quantidade = data.quantidades[ingressoId] || 0;
                elemento.textContent = quantidade;
            });
        })
        .catch(() => alert("Erro ao carregar o carrinho."));
}

function adicionarIngresso(ingressoId) {
    const quantidadeElement = document.getElementById(`quantidade-${ingressoId}`);
    
    fetch(`/adicionar_ao_carrinho/${ingressoId}/`, {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.sucesso) {
            quantidadeElement.textContent = data.quantidade;
            document.getElementById("total-carrinho").textContent = `R$ ${data.total}`;
        } else {
            alert(data.erro);
        }
    })
    .catch(() => alert("Erro ao adicionar ingresso"));
}

function removerIngresso(ingressoId) {
    const quantidadeElement = document.getElementById(`quantidade-${ingressoId}`);
    
    fetch(`/remover_do_carrinho/${ingressoId}/`, {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.sucesso) {
            quantidadeElement.textContent = data.quantidade;
            document.getElementById("total-carrinho").textContent = `R$ ${data.total}`;
        } else {
            alert(data.erro);
        }
    })
    .catch(() => alert("Erro ao remover ingresso"));
}
