from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento


def local_evento(request, titulo_evento):
    evento = Evento.objects.get(titulo=titulo_evento)
    return HttpResponse(evento.local)


def lista_eventos(request):
    usuario = request.user
    eventos = Evento.objects.all()
    dados = {'eventos':eventos}
    return render(request, 'agenda.html', dados)
