"""
Modelos principais do sistema de arrecadações.

Define as entidades utilizadas no sistema:
- CadastroModel: Cadastro simples de usuários.
- Cliente: Clientes registrados.
- Ong: Organizações não governamentais cadastradas.
- TipoDoacao: Tipos possíveis de doações.
- ValorDoacao: Valores pré-definidos de doações.
- Doacao: Registro das doações realizadas.
"""

from django.db import models

class CadastroModel(models.Model):
    """
    Model para cadastro simples de usuários.

    Campos:
    - nome: Nome completo do usuário.
    - email: Email do usuário.
    - senha: Senha do usuário (não criptografada, apenas para exemplo).
    """

    nome = models.CharField("Nome", max_length=200)
    email = models.EmailField("Email")
    senha = models.CharField("Senha", max_length=50)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    """
    Model que representa um cliente registrado.

    Campos:
    - nome: Nome completo do cliente.
    - email: Email único do cliente.
    - senha: Senha do cliente (deve ser armazenada criptografada em produção).
    """

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Ong(models.Model):
    """
    Model que representa uma ONG.

    Campos:
    - nome: Nome da ONG.
    - chave_pix: Chave PIX para receber doações (única).
    - horario_funcionamento: Horário de funcionamento da ONG.
    - endereco: Endereço físico da ONG.
    - informacoes_adicionais: Informações extras sobre a ONG.
    """

    nome = models.CharField(max_length=100)
    chave_pix = models.CharField(max_length=20, unique=True)
    horario_funcionamento = models.CharField(max_length=100, default="24 horas")
    endereco = models.CharField(max_length=255, default="Endereço padrão")
    informacoes_adicionais = models.TextField(blank=True, null=True)


class TipoDoacao(models.Model):
    """
    Model que representa os tipos de doações possíveis.

    Campos:
    - nome: Nome do tipo de doação (ex: Dinheiro, Alimentos, Roupas, etc.)
    """

    nome = models.CharField(max_length=100, verbose_name="Nome do Tipo de Doação")

    def __str__(self):
        return self.nome


class ValorDoacao(models.Model):
    """
    Model que representa valores possíveis de doação.

    Campos:
    - valor: Valor da doação em R$.
    """

    valor = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Valor da Doação"
    )

    def __str__(self):
        return f"R$ {self.valor}"


class Doacao(models.Model):
    """
    Model que registra uma doação feita a uma ONG.

    Campos:
    - ong_nome: Nome da ONG beneficiada.
    - item_doado: Nome do item doado (pode ser em branco).
    - tipo_doacao: Tipo da doação (ex: dinheiro, alimentos).
    - valor_doacao: Valor monetário da doação.
    - data_doacao: Data e hora da doação (gerado automaticamente).
    """

    ong_nome = models.CharField("Nome da ONG", max_length=100)
    item_doado = models.CharField("Item Doado", max_length=100, blank=True)
    tipo_doacao = models.CharField(
        "Tipo de Doação", max_length=100, default="Default Tipo"
    )
    valor_doacao = models.DecimalField(
        "Valor da Doação", max_digits=8, decimal_places=2, default=0.00
    )
    data_doacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ong_nome} - {self.item_doado}"
