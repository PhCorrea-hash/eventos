from .forms import LoginForms, CadastroForms

def login_form_processor(request):
    return {
        'form_login': LoginForms()
    }

def cadastro_form(request):
    return {'form_cadastro': CadastroForms()}