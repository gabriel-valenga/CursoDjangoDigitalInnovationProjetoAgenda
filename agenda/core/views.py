from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http.response import Http404, JsonResponse


def local_evento(request, titulo_evento):
    evento_ = Evento.objects.get(titulo=titulo_evento)
    return HttpResponse(evento_.local)


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    eventos = Evento.objects.filter(usuario=usuario)
    dados = {'eventos': eventos}
    return render(request, 'agenda.html', dados)


def login_user(request):
    return render(request, 'login.html')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou senha inválido!')
        return redirect('/')


def logout_user(request):
    logout(request)
    return redirect('/')


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
        data = request.POST.get('data')
        local = request.POST.get('local')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id = request.POST.get('id')
        if id:
            evento_ = Evento.objects.get(id=id)
            if evento_.usuario == usuario:
                evento_.titulo = titulo
                evento_.data = data
                evento_.local = local
                evento_.descricao = descricao
                evento_.save()

        else:
            Evento.objects.create(titulo=titulo,
                                  data=data,
                                  local=local,
                                  descricao=descricao,
                                  usuario=usuario)
    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento_ = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento_.usuario:
        evento_.delete()
    else:
        raise Http404()
    return redirect('/')


@login_required(login_url='/login/')
def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento_ = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(evento_), safe=False)
