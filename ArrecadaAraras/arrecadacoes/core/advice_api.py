import requests
from googletrans import Translator


class AdviceAPI:
    """
    Classe para obter conselhos da API AdviceSlip e traduzi-los para português.

    Atributos:
        url (str): URL da API de conselhos.
        translator (Translator): Instância do tradutor do googletrans.
    """

    def __init__(self, url:str):
        """
        Inicializa a classe com a URL da API e cria o tradutor.

        Args:
            url (str): URL da API de conselhos.
        """
        self.url = url
        self.translator = Translator()

    def get_advice(self) -> str|None:
        """
        Obtém um conselho aleatório da API e traduz para português.

        Returns:
            str: Conselho traduzido para português, ou None em caso de erro.
        """
        try:
            response = requests.get(self.url, timeout=5) #add timeout
            if response.status_code == 200:
                data = response.json()
                advice_text = data["slip"]["advice"]

                # Traduzindo o conselho para o português
                translated_advice = self.translator.translate(
                    advice_text , src="en", dest="pt"
                ).text
                return translated_advice
            else:
                print(f"Erro na requisição. Código de status: {response.status_code}")
                return None
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None


if __name__ == "__main__":
    URL_API = "https://api.adviceslip.com/advice"
    api = AdviceAPI(URL_API)
    translated_advice = api.get_advice()
    print(translated_advice )  # Aqui você terá o conselho traduzido para o português
