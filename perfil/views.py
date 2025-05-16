from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .models import Perfil
from .forms import PerfilForm, UserForm, FotoPerfilForm
from django.http import JsonResponse

@login_required
def perfil_view(request):
    user = request.user

    # Verifica se o usuário já tem um perfil
    try:
        perfil = user.perfil
        print("Foto de perfil:", perfil.foto_perfil)
        print("URL da foto de perfil:", perfil.foto_perfil.url if perfil.foto_perfil else "Sem foto")
    except Perfil.DoesNotExist:
        # Cria o perfil automaticamente para evitar erros
        perfil = Perfil.objects.create(user=user)

    if request.method == 'POST':
        # Atualiza as informações do perfil
        user_form = UserForm(request.POST, instance=user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Informações atualizadas com sucesso!')
            return redirect('perfil')
        else:
            messages.error(request, 'Erro ao atualizar informações.')

        # Atualiza a senha, se fornecida
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha_atual and nova_senha and confirmar_senha:
            if nova_senha == confirmar_senha:
                if user.check_password(senha_atual):
                    user.set_password(nova_senha)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Senha atualizada com sucesso!')
                else:
                    messages.error(request, 'A senha atual está incorreta.')
            else:
                messages.error(request, 'As senhas não coincidem.')

    else:
        user_form = UserForm(instance=user)
        perfil_form = PerfilForm(instance=perfil)

    return render(request, 'perfil/perfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
        'perfil': perfil,
    })

@login_required
def editar_foto_perfil(request):
    if request.method == 'POST':
        form = FotoPerfilForm(request.POST, request.FILES, instance=request.user.perfil)
        
        if form.is_valid():
            form.save()  # Salva no Cloudinary
            messages.success(request, "Foto de perfil atualizada com sucesso!")
        else:
            messages.error(request, "Erro ao atualizar a foto de perfil. Verifique o arquivo e tente novamente.")

    # Redireciona para a página anterior ou para a página de perfil
    return redirect(request.META.get('HTTP_REFERER', '/'))