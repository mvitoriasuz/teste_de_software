from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Any
from .models import Cliente
from datetime import datetime

class CadastroClienteService:
    def cadastrar_cliente(
        self, nome: str, email: str, senha: str,) -> dict:
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
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["arrecadacoes"]
        self.collection = self.db["doacao_ong"]

    def fazer_doacao(self, cliente_id, ong_nome, tipo_doacao, valor_doacao):
        try:
            self.collection.insert_one({
                "cliente_id": cliente_id,
                "ong_nome": ong_nome,
                "tipo_doacao": tipo_doacao,
                "valor_doacao": valor_doacao,
                "data_doacao": datetime.now()
            })
            return {"success": "Doação registrada com sucesso."}
        except Exception as e:
            return {"error": str(e)}

    def listar_ultimas_doacoes(self, cliente_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        doacoes = self.collection.find({"cliente_id": cliente_id}).sort("data_doacao", -1).limit(limit)
        return list(doacoes)

    def listar_doacoes_por_cliente(self, cliente_id: str) -> List[Dict[str, Any]]:
        doacoes = self.collection.find({"cliente_id": cliente_id})
        return list(doacoes)
    
    def contar_doacoes(self, cliente_id):
        doacoes = self.collection.count_documents({"cliente_id": cliente_id})
        return doacoes