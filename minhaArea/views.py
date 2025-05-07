from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from eventos.models import Eventos
from minhaArea.models import Grupo, MensagemGrupo, Agenda
from .forms import GrupoForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
import calendar
from datetime import date
from collections import defaultdict
from django.utils import timezone

# Função para renderizar a página area.html
@login_required
def area(request):
    # Eventos favoritos e grupos
    eventos_favoritos = Eventos.objects.filter(favoritos=request.user)
    grupos = request.user.grupos.all()

    # Agenda do usuário
    agenda_items = Agenda.objects.filter(usuario=request.user).select_related('evento')

    # Eventos por data
    eventos_por_data = defaultdict(list)
    for item in agenda_items:
        d = item.evento.data.date()
        eventos_por_data[d].append(item.evento)

    # Meses em português
    meses_pt = [
        "", "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]

    # Data atual
    hoje = timezone.now()
    ano_atual = hoje.year
    mes_atual = hoje.month

    # Montar calendário de 12 meses a partir do mês atual
    calendario = []
    for i in range(13):  
        mes = (mes_atual + i - 1) % 12 + 1
        ano = ano_atual + ((mes_atual + i - 1) // 12)
        nome = f"{meses_pt[mes]}-{ano}"
        num_dias = calendar.monthrange(ano, mes)[1]
        dias = []

        for dia in range(1, num_dias + 1):
            dt = date(ano, mes, dia)
            dias.append({
                'day': dia,
                'date': dt,
                'events': eventos_por_data.get(dt, [])
            })

        calendario.append({
            'year': ano,
            'month': mes,
            'name': nome,
            'days': dias
        })

    return render(request, 'minhaArea/area.html', {
        'eventos_favoritos': eventos_favoritos,
        'grupos': grupos,
        'calendario': calendario,
    })

# Função para riar um novo grupo
@login_required
def criar_grupo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')

        if nome:  
            grupo = GrupoForm({
                'nome': nome,
                'descricao': descricao,
                'criador': request.user
            })
            
            if grupo.is_valid():
                novo_grupo = grupo.save(commit=False)
                novo_grupo.criador = request.user
                novo_grupo.save()
                novo_grupo.membros.add(request.user)
                return redirect('area')
            else:
                return JsonResponse({'success': False, 'errors': grupo.errors})
        else:
            return JsonResponse({'success': False, 'errors': 'Nome do grupo é obrigatório'})

    return JsonResponse({'success': False, 'errors': 'Método inválido'})

# Função para listar os membros do grupo
@login_required
def listar_membros(request):
    termo = request.GET.get('q', '').strip()
    if termo:
        membros = User.objects.filter(username__icontains=termo).exclude(id=request.user.id).values('id', 'username')
    else:
        membros = User.objects.exclude(id=request.user.id).values('id', 'username')
    
    return JsonResponse({'success': True, 'membros': list(membros)})

# Função para adicionar membros ao grupo
@login_required
def adicionar_membro(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            grupo.membros.add(user)
            messages.success(request, f"{username} foi adicionado ao grupo com sucesso!")
        except User.DoesNotExist:
            messages.error(request, f"O usuário {username} não existe.")

    return redirect('area')  # redireciona para a área do usuário

# Função para renderizar a página do chat do grupo
def pagina_grupo(request, grupo_id):
    # Busca o grupo pelo ID
    grupo = get_object_or_404(Grupo, id=grupo_id)
    
    # Buscar todas as mensagens do grupo, ordenadas pela data de envio
    mensagens = MensagemGrupo.objects.filter(grupo=grupo).order_by('data_envio')
    eventos = Eventos.objects.filter(publicada=True)

    # Se o formulário for enviado, cria uma nova mensagem
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        MensagemGrupo.objects.create(grupo=grupo, usuario=request.user, conteudo=conteudo)
        return redirect('pagina_grupo', grupo_id=grupo.id)

    return render(request, 'minhaArea/pagina_grupo.html', {
        'grupo': grupo,
        'mensagens': mensagens,
        'eventos': eventos,
    })

#Função para o tratamento de mensagens
def adicionar_mensagem(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)

    if request.method == 'POST':
        texto = request.POST.get('texto')
        evento_id = request.POST.get('evento_id')

        mensagem = MensagemGrupo.objects.create(
            grupo=grupo,
            autor=request.user,
            texto=texto
        )

        if evento_id:
            evento = get_object_or_404(Eventos, id=evento_id)
            mensagem.evento = evento
            mensagem.save()
    
    return redirect('pagina_grupo', grupo_id=grupo.id)

# Função para adicionar um evento na agenda
@login_required
def adicionar_agenda(request, evento_id):
    if request.method != 'POST':
        return redirect('area')

    evento = get_object_or_404(Eventos, id=evento_id)

    adicionar_site = 'adicionar_site' in request.POST or 'adicionar_tudo' in request.POST

    # 1) Agenda interna do site
    if adicionar_site:
        Agenda.objects.get_or_create(usuario=request.user, evento=evento)

    return redirect('area')

# Função para remover um evento da agenda
@login_required
def remover_da_agenda(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)
    Agenda.objects.filter(usuario=request.user, evento=evento).delete()
    return redirect('area')