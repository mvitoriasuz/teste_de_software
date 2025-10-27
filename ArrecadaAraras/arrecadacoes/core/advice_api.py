import requests
from googletrans import Translator

class AdviceAPI:
    def __init__(self, url):
        self.url = url
        self.translator = Translator()

    def get_advice(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                data = response.json()
                advice = data['slip']['advice']

                # Traduzindo o conselho para o português
                translated_advice = self.translator.translate(advice, src='en', dest='pt').text
                return translated_advice
            else:
                print(f"Erro na requisição. Código de status: {response.status_code}")
                return None
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None

URL_API = "https://api.adviceslip.com/advice"

api = AdviceAPI(URL_API)
advice = api.get_advice()
print(advice)  # Aqui você terá o conselho traduzido para o português
