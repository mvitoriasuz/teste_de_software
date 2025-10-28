from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Any
from .models import Cliente
from datetime import datetime


class CadastroClienteService:
    """
    Serviço responsável por cadastrar novos clientes no sistema.

    Métodos:
        cadastrar_cliente(nome, email, senha): Cadastra um novo cliente no banco relacional.
    """

    def cadastrar_cliente(
        self,
        nome: str,
        email: str,
        senha: str,
    ) -> dict:
        """
        Cadastra um novo cliente no banco de dados relacional.

        Args:
            nome (str): Nome completo do cliente.
            email (str): Endereço de e-mail do cliente.
            senha (str): Senha escolhida pelo cliente.

        Returns:
            dict: Mensagem de sucesso ou erro do cadastro.
        """
        try:
            cliente = Cliente.objects.create(
                nome=nome,
                email=email,
                senha=senha,
            )
            return {"success": "Cliente cadastrado com sucesso."}
        except Exception as e:
            return {"error": str(e)}


class LogarUsuarioService:
    """
    Serviço responsável por registrar e consultar doações no banco MongoDB.

    Atributos:
        client (MongoClient): Conexão com o MongoDB.
        db (Database): Banco de dados 'arrecadacoes'.
        collection (Collection): Coleção 'doacao_ong' onde as doações são armazenadas.

    Métodos:
        fazer_doacao(): Registra uma nova doação.
        listar_ultimas_doacoes(): Retorna as últimas doações de um cliente.
        listar_doacoes_por_cliente(): Lista todas as doações de um cliente.
        contar_doacoes(): Conta o total de doações de um cliente.
    """

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["arrecadacoes"]
        self.collection = self.db["doacao_ong"]

    def fazer_doacao(self, cliente_id, ong_nome, tipo_doacao, valor_doacao):
        """
        Registra uma nova doação na coleção 'doacao_ong'.

        Args:
            cliente_id (str): ID do cliente que realiza a doação.
            ong_nome (str): Nome da ONG beneficiada.
            tipo_doacao (str): Tipo da doação (ex: dinheiro, alimento, roupa).
            valor_doacao (float): Valor monetário da doação.

        Returns:
            dict: Mensagem de sucesso ou erro ao registrar a doação.
        """
        try:
            self.collection.insert_one(
                {
                    "cliente_id": cliente_id,
                    "ong_nome": ong_nome,
                    "tipo_doacao": tipo_doacao,
                    "valor_doacao": valor_doacao,
                    "data_doacao": datetime.now(),
                }
            )
            return {"success": "Doação registrada com sucesso."}
        except Exception as e:
            return {"error": str(e)}

    def listar_ultimas_doacoes(
        self, cliente_id: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retorna as últimas doações realizadas por um cliente.

        Args:
            cliente_id (str): ID do cliente.
            limit (int): Número máximo de registros retornados (padrão: 5).

        Returns:
            list[dict]: Lista das últimas doações.
        """
        doacoes = (
            self.collection.find({"cliente_id": cliente_id})
            .sort("data_doacao", -1)
            .limit(limit)
        )
        return list(doacoes)

    def listar_doacoes_por_cliente(self, cliente_id: str) -> List[Dict[str, Any]]:
        """
        Lista todas as doações realizadas por um cliente.

        Args:
            cliente_id (str): ID do cliente.

        Returns:
            list[dict]: Lista completa das doações.
        """
        doacoes = self.collection.find({"cliente_id": cliente_id})
        return list(doacoes)

    def contar_doacoes(self, cliente_id):
        """
        Conta o número total de doações feitas por um cliente.

        Args:
            cliente_id (str): ID do cliente.

        Returns:
            int: Quantidade total de doações.
        """
        doacoes = self.collection.count_documents({"cliente_id": cliente_id})
        return doacoes
