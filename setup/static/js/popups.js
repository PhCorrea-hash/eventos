document.addEventListener("DOMContentLoaded", () => {
    const get = (selector) => document.querySelector(selector);

    const popups = {
        cadastro: get("#popup-cadastro"),
        criarGrupo: get("#popup-criargrupo"),
        favoritos: get("#popup-favoritos"),
        grupos: get("#popup-grupos"),
        login: get("#popup-login"),
        sugestoes: get("#popup-sugestoes"),
    };

    console.log(popups);
    

    function abrirPopup(popup) {
        if (!popup) {
            console.error("Popup não encontrado!");
            return;
        }
        fecharTodosPopups();
        popup.style.display = "flex";
    }

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

    document.querySelectorAll(".login").forEach(btn =>
        btn.addEventListener("click", () => {
            fecharTodosPopups();
            abrirPopup(popups.login);
        })
    );

    const btnLoginDentroCadastro = document.getElementById("popUpLoginDentroCadastro");
    if (btnLoginDentroCadastro) {
    btnLoginDentroCadastro.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        abrirPopup(popups.login);
    });
    }

    const btnCadastroDentroLogin = document.getElementById("popUpCadastroDentroLogin");
    if (btnCadastroDentroLogin) {
    btnCadastroDentroLogin.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        console.log("Botão do popup de login clicado");
        abrirPopup(popups.cadastro);
    });
    }

    const btnMostrarTodosFavoritos = document.getElementById("mostrar-todos-favoritos");
    if (btnMostrarTodosFavoritos) {
        btnMostrarTodosFavoritos.addEventListener("click", (event) => {
            event.preventDefault();
            event.stopPropagation();
            abrirPopup(popups.favoritos);
        });
    }

    const btnMostrarTodosGrupos = document.getElementById("mostrar-todos-grupos");
    if (btnMostrarTodosGrupos) {
        btnMostrarTodosGrupos.addEventListener("click", (event) => {
            event.preventDefault();
            event.stopPropagation();
            abrirPopup(popups.grupos);
        });
    }
});

