from django.shortcuts import render

from django.shortcuts import render, redirect
from usuarios.forms import LoginForms, CadastroForms
from django.contrib.auth.models import User
from django.contrib import auth, messages

def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            nome = form["nome_login"].value()
            senha = form["senha"].value()

            usuario = auth.authenticate(
                request,
                username=nome,
                password=senha
            )

            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, f"Bem-vindo(a) de volta, {nome}!")
            else:
                messages.error(request, "Erro ao efetuar o login: usuário ou senha inválidos.")
        else:
            messages.error(request, "Preencha os campos corretamente.")

        # Redireciona para a página de onde veio o request
        referer = request.META.get('HTTP_REFERER', '/')
        return redirect(referer)

    # Se for GET (alguém acessou diretamente a URL /login), redireciona para home
    return redirect('index')  # ou qualquer página principal do site

def cadastro(request):

    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)
        
        if form.is_valid():
            
            nome = form["nome_cadastro"].value()
            email = form["email"].value()
            senha = form["senha_1"].value()

            if User.objects.filter(username=nome).exists():
                messages.error(request, "Usuário já existente")
                return redirect('cadastro')
            
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            usuario.save()
            messages.success(request, "Cadastro realizado com sucesso")


    return redirect(request.META.get('HTTP_REFERER', '/'))

def logout(request):
    auth.logout(request)
    messages.success(request, "Logout efetuado com sucesso")
    return redirect('login')
