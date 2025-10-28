import re  # imports padrão primeiro
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CadastroModel
from .services import CadastroClienteService
from .models import Doacao


class CadastroForm(forms.ModelForm):
    """
    Formulário para cadastro de clientes.

    Realiza validações personalizadas nos campos nome, email e senha.
    Possui método 'registrar_cliente' que integra com o serviço de cadastro
    e cria o usuário no Django auth, exibindo mensagens de sucesso ou erro.
    """

    class Meta:
        model = CadastroModel
        fields = ["nome", "email", "senha"]
        widgets = {
            "senha": forms.PasswordInput(),
        }
        error_messages = {
            "nome": {"required": "Erro ao informar o campo nome."},
            "email": {"required": "Erro ao informar o campo email."},
            "senha": {"required": "Erro ao informar o campo senha."},
        }

    def clean_nome(self):
        """Normaliza o nome capitalizando todas as palavras."""
        nome = self.cleaned_data["nome"]
        palavras = [w.capitalize() for w in nome.split()]
        return " ".join(palavras)

    def clean_email(self):
        """Valida se o email possui formato correto."""
        email = self.cleaned_data["email"]
        if len(re.findall(r"@", email)) != 1 or len(re.findall(r"\.", email)) == 0:
            raise ValidationError("Por favor, insira um email válido.")
        return email

    def clean_senha(self):
        """
        Valida a senha para atender aos critérios de segurança:
        - mínimo de 8 caracteres
        - pelo menos uma letra maiúscula
        - pelo menos um caractere especial
        """
        senha = self.cleaned_data["senha"]

        if len(senha) < 8:
            raise ValidationError("Sua senha deve ter pelo menos 10 caracteres.")

        if not any(char.isupper() for char in senha):
            raise ValidationError(
                "Sua senha deve conter pelo menos uma letra maiúscula."
            )

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            raise ValidationError(
                "Sua senha deve conter pelo menos um caractere especial."
            )

        return senha

    def registrar_cliente(self, request):
        """
        Registra o cliente usando o serviço de cadastro.

        Cria um usuário no Django auth e retorna o resultado do serviço.
        Exibe mensagem de sucesso em caso de cadastro bem-sucedido.
        """
        data = self.cleaned_data
        cadastro_service = CadastroClienteService()
        resultado = cadastro_service.cadastrar_cliente(
            nome=data["nome"],
            email=data["email"],
            senha=data["senha"],
        )
        if "error" in resultado:
            raise ValidationError(resultado["error"])

        User.objects.create_user(
            username=data["email"], email=data["email"], password=data["senha"]
        )

        messages.success(request, "Cadastro realizado com sucesso!")
        return resultado


class LoginForm(forms.Form):
    """
    Formulário de login para usuários existentes.
    """

    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)


class DoacaoForm(forms.ModelForm):
    """
    Formulário para registro de doações.

    Campos ocultos são preenchidos automaticamente com informações da ONG e tipo/valor da doação.
    """

    class Meta:
        model = Doacao
        fields = ["ong_nome", "tipo_doacao", "valor_doacao"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ong_nome"].widget = forms.HiddenInput()
        self.fields["tipo_doacao"].widget = forms.HiddenInput()
        self.fields["valor_doacao"].widget = forms.HiddenInput()
