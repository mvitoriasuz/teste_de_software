# 🕊️ Arrecada Araras

O **Arrecada Araras** é um sistema web desenvolvido para facilitar a **arrecadação de doações** para ONGs da cidade de Araras.  
Criado em **Python (Django)**, o projeto segue boas práticas de desenvolvimento, organização e qualidade de código.

## ⚙️ Tecnologias Utilizadas

- 🐍 **Python 3**  
- 🌐 **Django Framework**  
- 🎨 **HTML5, CSS3 e Bootstrap**  
- 🧩 **MongoDB**   
- 🧪 **unittest e Coverage** (para testes automatizados)  
- 🧱 **Git & GitHub**  
- ⚙️ **legacy-cgi** *(para compatibilidade com Python 3.13+)*  

## 🚀 Como Executar o Projeto

### 1️⃣ Clonar o repositório
```console
git clone https://github.com/mvitoriasuz/PI-ArrecadaAraras.git
cd arrecadacoes/
python -m venv env
cd env/Scripts
activate.bat
cd ../..

2️⃣ Instalar as dependências
pip install -r requirements.txt
⚠️ Caso use Python 3.13 ou superior, instale também:
pip install legacy-cgi

3️⃣ Executar as migrações do banco de dados
cd arrecadacoes/
python manage.py migrate

4️⃣ (Opcional) Executar os testes
python manage.py test

5️⃣ (Opcional) Gerar relatório de cobertura
pip install coverage
coverage run --source='.' manage.py test 
coverage html

6️⃣ Iniciar o servidor
python manage.py runserver
Acesso ao sistema:
http://127.0.0.1:8000/

⚙️ Criar Superusuário
python manage.py createsuperuser
Acesso ao painel admin:
http://127.0.0.1:8000/admin
```


### 🧩 Análise de Qualidade e Segurança
O projeto Arrecada Araras segue práticas de qualidade de código e segurança, utilizando as ferramentas Pylint e Bandit.
> 🧠 Pylint — Análise de Qualidade de Código
O Pylint verifica se o código segue o padrão PEP8, além de identificar más práticas e possíveis erros de estilo ou lógica.

➤ Como executar:
```console
pylint --rcfile=.pylintrc core > pylint_report.txt
```

🛡️ Bandit — Análise de Segurança de Código

> O Bandit é uma ferramenta de análise estática voltada à identificação de vulnerabilidades em código Python.
Ele verifica riscos como uso de funções perigosas (eval, exec), comandos de sistema, e manipulação insegura de dados.

➤ Como executar:
```console
bandit -r core -f txt -o bandit_report.txt
```
