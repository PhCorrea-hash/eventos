// Variáveis para os elementos principais
const botaoAdicionarMembros = document.querySelector('.adicionar-membros');
const listaMembrosAdicionar = document.querySelector('.lista-membros-adicionar');
const campoPesquisa = document.getElementById('pesquisa-membros');
const membrosIdsInput = document.getElementById('membros-ids');
let listaMembrosTemp = [];  
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
                if (!listaMembrosTemp.some(tempMembro => tempMembro.id === membro.id)) {
                    const li = document.createElement('li');
                    li.textContent = membro.username;
                    li.setAttribute('data-id', membro.id);
                    li.addEventListener('click', (event) => adicionarMembro(membro, event));
                    listaMembrosAdicionar.appendChild(li);
                }
            });

            listaMembrosAdicionar.style.display = data.membros.length > 0 ? 'block' : 'none';
        }
    } catch (error) {
        console.error('Erro ao buscar membros:', error);
    }
}

// Função para adicionar membro ao grupo (visualmente)
function adicionarMembro(membro, event) {
    event.stopPropagation();

    if (!listaMembrosTemp.some(tempMembro => tempMembro.id === membro.id)) {
        listaMembrosTemp.push(membro);
        atualizarListaMembrosTemp();
    }

    const membroLi = document.querySelector(`[data-id="${membro.id}"]`);
    if (membroLi) {
        membroLi.remove();
    }

    // Atualiza o campo hidden com os IDs dos membros
    membrosIdsInput.value = listaMembrosTemp.map(m => m.id).join(',');
}

// Função para atualizar a lista de membros temporários
function atualizarListaMembrosTemp() {
    const listaTempContainer = document.getElementById('lista-membros-temp');
    listaTempContainer.innerHTML = '';  

    listaMembrosTemp.forEach(membro => {
        const li = document.createElement('li');
        li.textContent = membro.username;
        li.setAttribute('data-id', membro.id);
        li.style.backgroundColor = '#D3F9D8';  

        li.addEventListener('click', (event) => removerMembroTemp(membro, event));
        listaTempContainer.appendChild(li);
    });

    // Atualiza o campo hidden com os IDs dos membros
    membrosIdsInput.value = listaMembrosTemp.map(m => m.id).join(',');
}

// Função para remover membro da lista temporária
function removerMembroTemp(membro, event) {
    event.stopPropagation();
    listaMembrosTemp = listaMembrosTemp.filter(tempMembro => tempMembro.id !== membro.id);
    atualizarListaMembrosTemp();
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