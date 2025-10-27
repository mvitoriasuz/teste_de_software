from django.contrib import admin
from .models import Ong, TipoDoacao, ValorDoacao

class OngAdmin(admin.ModelAdmin):
    list_display = ('nome', 'chave_pix', 'horario_funcionamento', 'endereco')
    search_fields = ('nome', 'chave_pix')
    list_filter = ('horario_funcionamento',)


@admin.register(ValorDoacao)
class ValorDoacaoAdmin(admin.ModelAdmin):
    list_display = ['valor']

admin.site.register(Ong, OngAdmin)

admin.site.register(TipoDoacao)



