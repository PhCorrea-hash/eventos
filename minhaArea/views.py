from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from eventos.models import Eventos
from minhaArea.models import Grupo, MensagemGrupo, Agenda, GoogleCredentials
from .forms import GrupoForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
import calendar
from datetime import date, timedelta
from collections import defaultdict
from django.utils import timezone
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import os
import json
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.conf import settings


@login_required
def area(request):
    # Eventos favoritos e grupos
    eventos_favoritos = Eventos.objects.filter(favoritos=request.user)
    grupos = request.user.grupos.all()

    # Agenda do usuário
    agenda_items = Agenda.objects.filter(usuario=request.user).select_related('evento')

    # Agrupando eventos por data
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

    # Monta calendário de 12 meses a partir do mês atual
    calendario = []
    for i in range(13):  # De abril até abril do ano seguinte
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

    google_connected = SocialAccount.objects.filter(
        user=request.user,
        provider='google'
    ).exists()

    return render(request, 'minhaArea/area.html', {
        'eventos_favoritos': eventos_favoritos,
        'grupos': grupos,
        'calendario': calendario,
        'google_connected': google_connected,
    })

@login_required
def criar_grupo(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.criador = request.user
            grupo.save()
            grupo.membros.add(request.user)
            return redirect('area')  # ou para uma página do grupo
    else:
        form = GrupoForm()

    return render(request, 'minhaArea/criar_grupo.html', {'form': form})

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

@login_required
def adicionar_agenda(request, evento_id):
    if request.method != 'POST':
        return redirect('area')

    evento = get_object_or_404(Eventos, id=evento_id)

    adicionar_site   = 'adicionar_site'   in request.POST
    adicionar_google = 'adicionar_google' in request.POST
    adicionar_tudo   = 'adicionar_tudo'   in request.POST

    # 1) Agenda interna do site
    if adicionar_site or adicionar_tudo:
        Agenda.objects.get_or_create(usuario=request.user, evento=evento)

    # 2) Agenda Google via allauth SocialToken
    if adicionar_google or adicionar_tudo:
        try:
            # encontra a conta social do Google
            social_account = SocialAccount.objects.get(
                user=request.user,
                provider='google'
            )
            # e o token associado
            social_token = SocialToken.objects.get(account=social_account)
        except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist):
            messages.error(request, "Você precisa primeiro conectar sua conta Google.")
            return redirect('area')

        # monta as credenciais a partir do token e do refresh_token
        creds = Credentials(
            token=social_token.token,                # access_token
            refresh_token=social_token.token_secret, # refresh_token
            token_uri='https://oauth2.googleapis.com/token',
            client_id=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            scopes=['https://www.googleapis.com/auth/calendar']
        )

        service = build('calendar', 'v3', credentials=creds)

        start = evento.data.isoformat()
        end   = (evento.data + timedelta(hours=1)).isoformat()

        body = {
            'summary':     evento.nome,
            'location':    evento.local or '',
            'description': evento.descricao,
            'start':  {'dateTime': start, 'timeZone': 'America/Sao_Paulo'},
            'end':    {'dateTime': end,   'timeZone': 'America/Sao_Paulo'},
        }
        service.events().insert(calendarId='primary', body=body).execute()
        messages.success(request, "Evento adicionado ao Google Calendar!")
    
    return redirect('area')

@login_required
def remover_da_agenda(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)
    Agenda.objects.filter(usuario=request.user, evento=evento).delete()
    return redirect('area')

# Carrega seu credentials.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'root/credentials.json')) as f:
    CLIENT_SECRETS = json.load(f)

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
REDIRECT_URI = 'http://localhost:8000/oauth2callback/'  # deve bater com o console

def init_google_calendar(request):
    flow = Flow.from_client_config(
        CLIENT_SECRETS,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    request.session['flow'] = flow
    return redirect(auth_url)

def oauth2callback(request):
    flow = request.session.get('flow')
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    # Salve `credentials.to_json()` no seu modelo GoogleCredentials
    GoogleCredentials.objects.update_or_create(
        user=request.user,
        defaults={'credentials': credentials.to_json()}
    )
    return redirect('area')

