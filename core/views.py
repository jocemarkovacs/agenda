from datetime import datetime, timedelta
from django.shortcuts import render, redirect   
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http.response import Http404, JsonResponse

# Create your views here.
# def index(request):
#     return redirect('/agenda/')

def submit_login(request):
    if request.POST:        
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário e/o Senha Inválido(s)")

    return redirect('/')

def logout_user(request):
    logout(request)    
    return redirect('/')

def login_user(request):
    return render(request, 'login.html')


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    #__gt representa maior __lt representa menor
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt=data_atual)
    eventos = Evento.objects.filter(usuario=usuario) # filtra por usuário passado
    # eventos = Evento.objects.all() # Mostra todos os usuários
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)

    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')        
        local_evento = request.POST.get('local_evento')
        usuario = request.user        
        print(f'Local: {local_evento}')
        print(f'Descrição: {descricao}')
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            #está fazendo uma validação se  usuário que está no BD é igual ao usuário informado vindo pelo metodo POST
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.data_evento = data_evento
                evento.descricao = descricao
                evento.local_evento = local_evento
                evento.save()
            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                             data_evento=data_evento,
            #                                             descricao=descricao,
            #                                             local=local)
        else:
            Evento.objects.create(titulo=titulo,
                                data_evento=data_evento,
                                descricao=descricao,
                                usuario=usuario,
                                local_evento=local_evento)
        
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user

    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404
    
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    
    return redirect('/')

## para retornar um Json
@login_required(login_url='/login/')
def json_lista_evento(request):
    
    usuario = request.user    
    # Passando dados do evento via Json. Importante notar quê:
    # - evento é um objeto do tipo QuerySet e deve ser transformado em uma lista. 
    # - values é para extrair os valores do objeto.
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo', 'data_evento')  
        
    # - importante passar o parametro safe=False, pois ele espera como parametro um dict,
    # mas será passado uma lista contendo um dict.
    return JsonResponse(list(evento), safe=False)

#retornar para uma api através do id. Note que como é para ser consumido,
# ele não requer uma autenticação através Http. Essa autenticação deve ser
# feita anteriormente e diretamente na Aplicação que consumirá.
def json_lista_evento_api(request, id_usuario):
    
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')  

    return JsonResponse(list(evento), safe=False)
