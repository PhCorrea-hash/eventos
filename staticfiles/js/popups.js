document.addEventListener("DOMContentLoaded", () => {
    const get = (selector) => document.querySelector(selector);

    // lista com todos os popups
    const popups = {
        cadastro: get("#popup-cadastro"),
        criarGrupo: get("#popup-criargrupo"),
        favoritos: get("#popup-favoritos"),
        grupos: get("#popup-grupos"),
        login: get("#popup-login"),
        sugestoes: get("#popup-sugestoes"),
    };

    // Função principal para abrir os popups
    function abrirPopup(popup) {
        if (!popup) {
            console.error("Popup não encontrado!");
            return;
        }
        fecharTodosPopups();
        popup.style.display = "flex";
    }

    // Função principal para fechar os popups
    function fecharTodosPopups() {
        Object.values(popups).forEach(popup => {
            if (popup) popup.style.display = "none";
        });
    }

    // Fecha popups ao clicar fora
    window.addEventListener("click", (e) => {
        Object.values(popups).forEach(popup => {
            if (popup && popup.style.display === "flex" && !popup.contains(e.target)) {
                fecharTodosPopups();
            }
        });
    });

    // Botão do menu lateral: Login
    const btnLogin = document.getElementById("popUpLogin-btn");
    if (btnLogin) {
        btnLogin.addEventListener("click", function(event) {
            event.stopPropagation();
            console.log("clicou no login");
            abrirPopup(popups.login);
        });
    }

    // Botão de cadastro no menu lateral 
    const btnCadastro = document.getElementById("popUpCadastro-btn");
    if (btnCadastro) {
        btnCadastro.addEventListener("click", function(event) {
            event.stopPropagation();
            console.log("clicou no cadastro");
            abrirPopup(popups.cadastro);
        });
    }

    // Alternar entre login e cadastro dentro dos popups
    document.querySelectorAll(".cadastrar-popup").forEach(btn =>
        btn.addEventListener("click", () => {
            fecharTodosPopups();
            abrirPopup(popups.cadastro);
        })
    );

    // Alternar entre login e cadastro dentro dos popups
    document.querySelectorAll(".login").forEach(btn =>
        btn.addEventListener("click", () => {
            fecharTodosPopups();
            abrirPopup(popups.login);
        })
    );

    // Alternar entre login e cadastro dentro dos popups
    const btnLoginDentroCadastro = document.getElementById("popUpLoginDentroCadastro");
    if (btnLoginDentroCadastro) {
    btnLoginDentroCadastro.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        abrirPopup(popups.login);
    });
    }

    // Alternar entre login e cadastro dentro dos popups
    const btnCadastroDentroLogin = document.getElementById("popUpCadastroDentroLogin");
    if (btnCadastroDentroLogin) {
    btnCadastroDentroLogin.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        console.log("Botão do popup de login clicado");
        abrirPopup(popups.cadastro);
    });
    }

    // Mostrar o popup dos eventos favoritos
    const btnMostrarTodosFavoritos = document.getElementById("mostrar-todos-favoritos");
    if (btnMostrarTodosFavoritos) {
        btnMostrarTodosFavoritos.addEventListener("click", (event) => {
            event.preventDefault();
            event.stopPropagation();
            abrirPopup(popups.favoritos);
        });
    }

    // Mostrar o popup dos grupos
    const btnMostrarTodosGrupos = document.getElementById("mostrar-todos-grupos");
    if (btnMostrarTodosGrupos) {
        btnMostrarTodosGrupos.addEventListener("click", (event) => {
            event.preventDefault();
            event.stopPropagation();
            abrirPopup(popups.grupos);
        });
    }

    // Mostrar o popup de cração de grupo
    const btnCriarGrupo = document.getElementById("btn-criar-grupo");
    if (btnCriarGrupo) {
        btnCriarGrupo.addEventListener("click", (event) => {
            event.preventDefault();
            event.stopPropagation();
            abrirPopup(popups.criarGrupo);
        })
    }

    // Alterar entre o popup de grupos e o popup de criação de grupo
    const abrirPopupCriarGrupo = document.getElementById("abrirPopupCriarGrupo");
    if (abrirPopupCriarGrupo) {
        abrirPopupCriarGrupo.addEventListener("click", (event) => {
            event.preventDefault();
            event.stopPropagation();
            fecharTodosPopups();
            abrirPopup(popups.criarGrupo);
        })
    }
});



