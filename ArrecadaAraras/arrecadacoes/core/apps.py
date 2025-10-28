from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuração da aplicação 'core' do projeto Arrecadacoes.

    Define o nome da aplicação e o tipo de campo padrão para chaves primárias.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
