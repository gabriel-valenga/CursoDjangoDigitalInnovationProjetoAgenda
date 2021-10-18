from django.contrib import admin
from core.models import Evento


class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'datacriacao')
    list_filter = ('usuario', 'data')


admin.site.register(Evento, EventoAdmin)
