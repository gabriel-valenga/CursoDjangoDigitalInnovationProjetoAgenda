from django.shortcuts import render, HttpResponse
from core.models import Evento


def local_evento(request, titulo_evento):
    evento = Evento.objects.get(titulo=titulo_evento)
    return HttpResponse(evento.local)
