// Variáveis para os elementos principais
const botaoAdicionarMembros = document.querySelector('.adicionar-membros');
const listaMembrosAdicionar = document.querySelector('.lista-membros-adicionar');
const campoPesquisa = document.getElementById('pesquisa-membros');
let listaMembrosTemp = [];  // Lista de membros temporários
let debounceTimeout;

// Função para buscar usuários disponíveis
async function buscarMembros(termo = '') {
    try {
        if (termo.trim() === '') {
            listaMembrosAdicionar.style.display = 'none';
            return;
        }

        const response = await fetch(`/membros?q=${encodeURIComponent(termo)}`);
        const data = await response.json();

        if (data.success) {
            listaMembrosAdicionar.innerHTML = ''; 

            // Preenche a lista com os membros encontrados
            data.membros.forEach(membro => {
                // Verifica se o membro já está na lista temporária, caso contrário, adiciona à lista
                if (!listaMembrosTemp.some(tempMembro => tempMembro.id === membro.id)) {
                    const li = document.createElement('li');
                    li.textContent = membro.username;
                    li.setAttribute('data-id', membro.id);
                    li.addEventListener('click', (event) => adicionarMembro(membro, event));
                    listaMembrosAdicionar.appendChild(li);
                }
            });

            // Mostra a lista apenas se houver resultados
            listaMembrosAdicionar.style.display = data.membros.length > 0 ? 'block' : 'none';
        }
    } catch (error) {
        console.error('Erro ao buscar membros:', error);
    }
}

// Função para adicionar membro ao grupo (visualmente)
function adicionarMembro(membro, event) {
    
    event.stopPropagation();

    // Se o membro já estiver na lista temporária, não faz nada
    if (!listaMembrosTemp.some(tempMembro => tempMembro.id === membro.id)) {
        // Adiciona o membro à lista temporária
        listaMembrosTemp.push(membro);
        atualizarListaMembrosTemp();
    }

    // Remove o membro da lista de busca ao ser clicado
    const membroLi = document.querySelector(`[data-id="${membro.id}"]`);
    if (membroLi) {
        membroLi.remove();
    }
}

// Função para atualizar a lista de membros temporários
function atualizarListaMembrosTemp() {
    const listaTempContainer = document.getElementById('lista-membros-temp');
    listaTempContainer.innerHTML = '';  

    // Adiciona os membros da lista temporária
    listaMembrosTemp.forEach(membro => {
        const li = document.createElement('li');
        li.textContent = membro.username;
        li.setAttribute('data-id', membro.id);
        li.style.backgroundColor = '#D3F9D8';  

        // Remove membro da lista temporária ao clicar
        li.addEventListener('click', (event) => removerMembroTemp(membro, event));

        listaTempContainer.appendChild(li);
    });
}

// Função para remover membro da lista temporária e re-adicionar à lista de pesquisa
function removerMembroTemp(membro, event) {
    // Previne a propagação do evento para o document, evitando que o popup feche
    event.stopPropagation();

    // Remove o membro da lista temporária
    listaMembrosTemp = listaMembrosTemp.filter(tempMembro => tempMembro.id !== membro.id);

    // Atualiza a lista de membros temporários
    atualizarListaMembrosTemp();

    // Re-adiciona o membro de volta à lista de pesquisa
    const li = document.createElement('li');
    li.textContent = membro.username;
    li.setAttribute('data-id', membro.id);
    li.addEventListener('click', (event) => adicionarMembro(membro, event));
    listaMembrosAdicionar.appendChild(li);
}

// Função de debounce para evitar múltiplas requisições rápidas
function debounceBuscarMembros(termo) {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => buscarMembros(termo), 300);
}

// Evento para abrir o campo de pesquisa ao clicar no botão
botaoAdicionarMembros.addEventListener('click', (event) => {
    event.preventDefault();
    campoPesquisa.style.display = 'block';
    campoPesquisa.focus();
});

// Evento para pesquisar membros com debounce
campoPesquisa.addEventListener('input', (event) => {
    const termo = event.target.value.trim();
    debounceBuscarMembros(termo);
});

// Fecha a lista ao clicar fora dela
document.addEventListener('click', (event) => {
    if (!event.target.closest('.adicionar-membros-container')) {
        listaMembrosAdicionar.style.display = 'none';
        campoPesquisa.value = '';
    }
});