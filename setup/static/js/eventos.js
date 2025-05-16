// busca dinâmica
const inputBusca = document.getElementById('busca');
const container = document.getElementById('eventos-container');
const body = document.getElementById('body'); 
   
// Buscar e mostrar evento
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
                        <div class="item-container">
                        <div class="imagem-btn"> 
                                <div class="evento-imagem-container">
                                    <a href="{% url 'detalhes_eventos' evento.id %}" class="evento-link">
                                        <img src="${evento.imagem}" alt="" class="evento-img">
                                    </a>
                                    <button 
                                        class="favorito-btn" 
                                        data-evento-id="${evento.id}">
                                        <img src="${evento.favorito ? '/static/assets/icons/favoritado-icon.png' : '/static/assets/icons/favoritar-icon.png'}" alt="" class="favoritar-icone">
                                    </button>
                                </div>
                            <button type="button"
                                    class="adicionar-agenda-btn"
                                    data-evento-id="${evento.id}"
                                    onclick="toggleOpcoesAgenda(${evento.id})">
                                    Adicionar à Agenda
                            </button>
                        </div>
                        <div class="evento-detalhes">
                            <h3 class="evento-detalhes-titulo">${evento.nome}</h3>
                            <div class="evento-detalhes-local">
                                <img src="/static/assets/icons/local-branco-icon.png" alt="" class="detalhes-icone">
                                <p class="detalhes-texto">${evento.legenda}</p>
                            </div>
                            <div class="evento-detalhes-data">
                                <img src="/static/assets/icons/calendario-branco-icon.png" alt="" class="detalhes-icone">
                                <p class="detalhes-texto">${evento.data}</p>
                            </div>
                        </div>
                    </div>
                    <div id="opcoes-agenda-${evento.id}"
                        class="opcoes-agenda">
                        <form method="post" action="{% url 'adicionar_agenda' evento.id %}" class="agenda-form">
                            {% csrf_token %}
                            <div class="form-container">
                                <label>
                                    <input type="checkbox" name="adicionar_site" checked>
                                        Adicionar à minha agenda personalizada
                                    </label><br>
                                    
                            </div>
                            <button type="submit" class="agenda-submit">Confirmar</button>
                        </form>
                    </div>
                    `;
                    container.appendChild(li);
                });
            });
    });
}

// botão de favoritar
document.querySelectorAll('.favorito-btn').forEach(button => {
    button.addEventListener('click', () => {
        if (body.classList.contains('user-logged-in')) {
            const eventoId = button.dataset.eventoId;  

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
    
                const icone = button.querySelector('.favoritar-icone');
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
        } else {
            alert("Faça login para continuar");
        }
    });
});

// Pegar evento a ser adicioniado à agenda
document.querySelectorAll('.adicionar-agenda-btn').forEach(button => {
    button.addEventListener('click', (e) => {
        const eventoId = e.target.getAttribute('data-evento-id');

        if (!eventoId) {
            console.error('ID do evento não encontrado!');
            return;
        }

        const modal = document.getElementById(`opcoes-agenda-${eventoId}`);

        if (modal) {
            // Ajusta a ação do formulário com o ID do evento
            modal.querySelector('form').action = `/adicionar-agenda/${eventoId}/`;
        } else {
            console.error(`Modal com ID opcoes-agenda-${eventoId} não encontrado.`);
        }
    });
});

// Opções de adicionar à agenda
function toggleOpcoesAgenda(id) {
    if (body.classList.contains('user-logged-in')) {
        const dropdown = document.getElementById(`opcoes-agenda-${id}`);
        if (!dropdown) return;

        const isVisible = dropdown.classList.contains('visivel');

        // Fecha todos e remove inline styles
        document.querySelectorAll('.opcoes-agenda').forEach(div => {
            div.classList.remove('visivel');
            div.style.display = '';  
        });

        if (!isVisible) {
            dropdown.style.display = ''; 
            dropdown.classList.add('visivel');
        }
    } else {
        alert("Faça login para continuar");
    }
}

// Adicionar evento à agenda
function adicionarAgenda(eventoId) {
    fetch("{% url 'adicionar_agenda' 0 %}".replace("0", eventoId))
        .then(response => response.json())
        .then(data => alert(data.mensagem));
}

// Fecha se clicar fora
document.addEventListener('click', function (event) {
    const isClickInside = event.target.closest('.info, .opcoes-agenda, .adicionar-agenda-btn');
    if (!isClickInside) {
        document.querySelectorAll('.opcoes-agenda').forEach(div => {
            div.style.display = 'none';
        });
    }
});

// Toggle do menu perfil no header
function toggleMenuPerfil() {
    const menu = document.querySelector('.menu-lateral-perfil');
    const botao = document.getElementById('botao-menu');
    const iconeUsuario = botao.querySelector('.icone-usuario');
    const iconeFechar = botao.querySelector('.icone-fechar');

    const isAtivo = menu.classList.toggle('ativo');
    botao.classList.toggle('ativo');

    if (isAtivo) {
        iconeUsuario.style.display = 'none';
        iconeFechar.style.display = 'inline';
    } else {
        iconeUsuario.style.display = 'inline';
        iconeFechar.style.display = 'none';
    }
}

// Fecha o menu clicando fora
document.addEventListener('click', function(event) {
    const menu = document.querySelector('.menu-lateral-perfil');
    const botao = document.getElementById('botao-menu');

    if (!menu.contains(event.target) && !botao.contains(event.target)) {
        menu.classList.remove('ativo');
        botao.classList.remove('ativo');

        const iconeUsuario = botao.querySelector('.icone-usuario');
        const iconeFechar = botao.querySelector('.icone-fechar');
        iconeUsuario.style.display = 'inline';
        iconeFechar.style.display = 'none';
    }
});


// Clicar em um dia na agenda e abrir um popup com os eventos correspondentes a ele
const dias = document.querySelectorAll('.dia');
const modal = document.getElementById('modal-dia');
const listaEventosDia = document.getElementById('lista-eventos-dia');
const fecharModal = document.getElementById('fechar-modal');

dias.forEach(dia => {
    dia.addEventListener('click', function () {
        const eventos = dia.querySelectorAll('.evento');
        listaEventosDia.innerHTML = ''; 

        eventos.forEach(evento => {
            const eventoId = evento.getAttribute('data-id');
            const eventoNome = evento.querySelector('.evento-nome').textContent;
            const eventoUrl = evento.getAttribute('data-url'); // Pega o link do evento a partir do atributo data-url
            const removerUrl = evento.querySelector('.remover-evento').getAttribute('href'); // Pega o link de remover

            const li = document.createElement('li');
            li.innerHTML = `
                <a href="${eventoUrl}">${eventoNome}</a>
                <a href="${removerUrl}" class="remover-evento" style="display:block;">Remover</a>
            `;
            listaEventosDia.appendChild(li);
        });

        modal.classList.remove('hidden');
    });
});

// Fechar modal
fecharModal.addEventListener('click', function () {
    modal.classList.add('hidden');
});

// Fechar modal clicando fora
modal.addEventListener('click', function (e) {
    if (e.target === modal) {
        modal.classList.add('hidden');
    }
});

