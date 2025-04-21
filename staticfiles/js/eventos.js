// busca dinâmica
const inputBusca = document.getElementById('busca');
const container = document.getElementById('eventos-container');

if (inputBusca) {
    inputBusca.addEventListener('input', function () {
        const query = inputBusca.value;

        fetch(`/buscar/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                container.innerHTML = '';

                if (data.length === 0) {
                    container.innerHTML = '<p>Nenhum evento encontrado.</p>';
                    return;
                }

                data.forEach(evento => {
                    const li = document.createElement('li');
                    li.classList.add('eventos-lista-item');
                    li.innerHTML = `
                        <a class="evento-link" href="${evento.link}">
                            <div class="imagem-container">
                                <img src="${evento.imagem}" class="imagem">
                                <div class="descricao-overlay">${evento.descricao}</div>
                            </div>
                        </a>
                        <h3 class="evento-titulo">${evento.nome}</h3>
                        <p class="evento-legenda">${evento.legenda}</p>
                        <p class="evento-data">${evento.data}</p>
                    `;
                    container.appendChild(li);
                });
            });
    });
}

// botão de favoritar
document.querySelectorAll('.favorito-btn').forEach(button => {
    button.addEventListener('click', () => {
        const eventoId = button.dataset.eventoId;  // Usa o ID do evento associado ao botão

        fetch(`/favoritar/${eventoId}/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (response.status === 401) {
                // Se não estiver logado, redireciona para a página de login
                window.location.href = '/login/';
                return;  // Interrompe a execução para não prosseguir com o código abaixo
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;  // Se não houver dados, retorna

            const icone = button.querySelector('.icone-favorito');
            if (data.favorited) {
                // Caso o evento seja favoritado, altera o ícone e a classe
                icone.src = '/static/assets/icons/favoritado-icon.png';
                button.classList.add('ativo');
            } else {
                // Caso contrário, volta o ícone para o estado inicial e remove a classe
                icone.src = '/static/assets/icons/favoritar-icon.png';
                button.classList.remove('ativo');
            }
        });
    });
});

document.querySelectorAll('.adicionar-agenda-btn').forEach(button => {
    button.addEventListener('click', (e) => {
        const eventoId = e.target.getAttribute('data-evento-id');
        const modal = document.getElementById('opcoes-agenda');
        modal.style.display = 'block';

        // Caso queira garantir que o formulário é enviado com o evento correto
        modal.querySelector('form').action = `/adicionar-agenda/${eventoId}/`;
    });
});

function toggleOpcoesAgenda(id) {
    const dropdown = document.getElementById(`opcoes-agenda-${id}`);
    const isVisible = dropdown.style.display === 'block';

    // Fecha todos os dropdowns antes
    document.querySelectorAll('.opcoes-agenda').forEach(div => {
        div.style.display = 'none';
    });

    // Abre o atual se ele não estiver visível
    if (!isVisible) {
        dropdown.style.display = 'block';
    }

    console.log("Clicou no botão de evento ID:", id);
}

// Fecha se clicar fora
document.addEventListener('click', function (event) {
    const isClickInside = event.target.closest('.info');
    if (!isClickInside) {
        document.querySelectorAll('.opcoes-agenda').forEach(div => {
            div.style.display = 'none';
        });
    }
});