from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone as djangotimezone


class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data = models.DateTimeField(verbose_name='Data do Evento')
    datacriacao = models.DateTimeField(auto_now=True, verbose_name='Data de Criação')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    local = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'evento'

    def __str__(self):
        return self.titulo

    def get_data(self):
        return self.data.strftime('%d/%m/%Y %H:%M')

    def get_data_input(self):
        return self.data.strftime('%Y-%m-%dT%H:%M')

    def get_evento_atrasado(self):
        if self.data < djangotimezone.now():
            return True
        else:
            return False

    def get_evento_inicio_proximo(self):
        if (self.data - djangotimezone.now()) <= timedelta(hours=1):
            return True
        else:
            return False
