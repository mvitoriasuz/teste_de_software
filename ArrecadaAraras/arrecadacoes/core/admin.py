"""
Configuração do Django Admin para o app 'core'.

Registra os modelos Ong, TipoDoacao e ValorDoacao no painel de administração
e define como eles devem ser exibidos e filtrados.
"""

from django.contrib import admin
from .models import Ong, TipoDoacao, ValorDoacao


class OngAdmin(admin.ModelAdmin):
    """Define exibição e filtros personalizados para o modelo Ong no admin Django."""

    list_display = ("nome", "chave_pix", "horario_funcionamento", "endereco")
    search_fields = ("nome", "chave_pix")
    list_filter = ("horario_funcionamento",)


@admin.register(ValorDoacao)
class ValorDoacaoAdmin(admin.ModelAdmin):
    """Exibe os valores de doação no painel administrativo."""

    list_display = ["valor"]


admin.site.register(Ong, OngAdmin)

admin.site.register(TipoDoacao)
