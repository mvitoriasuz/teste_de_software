from django.db import models

class CadastroModel(models.Model):
    nome = models.CharField('Nome', max_length=200)
    email = models.EmailField('Email')
    senha = models.CharField('Senha', max_length=50)

    def __str__(self):
        return self.nome
    

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome
    

class Ong(models.Model):
    nome = models.CharField(max_length=100)
    chave_pix = models.CharField(max_length=20, unique=True)
    horario_funcionamento = models.CharField(max_length=100, default='24 horas')
    endereco = models.CharField(max_length=255, default='Endereço padrão')
    informacoes_adicionais = models.TextField(blank=True, null=True)


class TipoDoacao(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome do Tipo de Doação')

    def __str__(self):
        return self.nome

class ValorDoacao(models.Model):
    valor = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Valor da Doação')

    def __str__(self):
        return f'R$ {self.valor}'
    
    
class Doacao(models.Model):
    ong_nome = models.CharField('Nome da ONG', max_length=100)
    item_doado = models.CharField('Item Doado', max_length=100, blank=True)
    tipo_doacao = models.CharField('Tipo de Doação', max_length=100, default='Default Tipo')
    valor_doacao = models.DecimalField('Valor da Doação', max_digits=8, decimal_places=2, default=0.00)
    data_doacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ong_nome} - {self.item_doado}"