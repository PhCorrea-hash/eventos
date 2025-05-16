document.getElementById('form-imagem-perfil').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio normal do formulário

    var formData = new FormData(this); // Cria um objeto FormData com os dados do formulário

    // Envia o formulário via POST para a view de editar a foto de perfil
    fetch("{% url 'editar_foto_perfil' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);  // Exibe a mensagem de sucesso
            document.getElementById('popup-imagem-perfil').style.display = 'none';  // Fecha o popup
            location.reload(); // Atualiza a página para refletir a nova foto de perfil
        } else {
            alert(data.message);  // Exibe a mensagem de erro
        }
    })
    .catch(error => {
        alert('Erro ao enviar a solicitação');
    });
});