"""Views principais do sistema de arrecadações.
Contém as rotas de cadastro, login, doações, perfil do usuário e integração com API externa.
"""

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CadastroForm, DoacaoForm, LoginForm
from .services import LogarUsuarioService
from .models import Ong, TipoDoacao, ValorDoacao
from .advice_api import AdviceAPI
from django.http import HttpResponse


def index(request):
    """Exibe a página inicial do sistema."""
    return render(request, "index.html")


def cadastro_view(request):
    """Gerencia o fluxo de cadastro de novos usuários."""
    if request.method == "POST":
        form_cadastro = CadastroForm(request.POST)
        if form_cadastro.is_valid():
            try:
                form_cadastro.registrar_cliente(request)
                return redirect("core:index")
            except ValidationError as e:
                form_cadastro.add_error(None, e.message)
    else:
        form_cadastro = CadastroForm()

    contexto = {"form_cadastro": form_cadastro}
    return render(request, "cadastro.html", contexto)


def login_view(request):
    """Realiza a autenticação do usuário e inicia a sessão."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login bem-sucedido.")
                return redirect(reverse("core:index"))
            else:
                return render(
                    request,
                    "login.html",
                    {"form": form, "error_message": "Credenciais inválidas."},
                )
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("core:index")


def ongs_view(request):
    """Exibe a lista de ONGs disponíveis e opções de doação."""
    ongs = Ong.objects.all()
    tipos_doacao = TipoDoacao.objects.all()
    valores_doacao = ValorDoacao.objects.all()

    contexto = {
        "ongs": ongs,
        "tipos_doacao": tipos_doacao,
        "valores_doacao": valores_doacao,
    }
    return render(request, "ongs.html", contexto)


@login_required
def doacao_view(request):
    """Gerencia o processo de doação, incluindo validação e registro."""
    if request.method == "POST":
        form = DoacaoForm(request.POST)
        if form.is_valid():
            ong_nome = form.cleaned_data["ong_nome"]
            tipo_doacao = request.POST.get("tipo_doacao")
            valor_doacao = request.POST.get("valor_doacao")

            cliente_id = request.user.id

            service = LogarUsuarioService()
            resultado = service.fazer_doacao(
                cliente_id, ong_nome, tipo_doacao, valor_doacao
            )

            if "success" in resultado:
                messages.success(request, "Doação registrada com sucesso.")
                return redirect("core:expired_screen")
            else:
                messages.error(request, resultado.get("error", "Erro ao fazer doação."))
        else:
            messages.error(
                request, "Dados inválidos. Verifique os campos obrigatórios."
            )
    else:
        form = DoacaoForm()

    ongs = Ong.objects.all()
    tipos_doacao = TipoDoacao.objects.all()
    valores_doacao = ValorDoacao.objects.all()

    return render(
        request,
        "ongs.html",
        {
            "form": form,
            "ongs": ongs,
            "tipos_doacao": tipos_doacao,
            "valores_doacao": valores_doacao,
        },
    )


@login_required
def meu_perfil(request):
    """Exibe o perfil do usuário, incluindo histórico e estatísticas de doações."""
    usuario = request.user
    service = LogarUsuarioService()

    doacoes_usuario = service.listar_doacoes_por_cliente(usuario.id)

    total_doacoes = sum(float(doacao["valor_doacao"]) for doacao in doacoes_usuario)
    qtd_doacoes = service.contar_doacoes(usuario.id)

    ultimas_doacoes = []
    for doacao in doacoes_usuario:
        ultimas_doacoes.append(
            {
                "ong_nome": doacao["ong_nome"],
                "tipo_doacao": doacao["tipo_doacao"],
                "valor_doacao": doacao["valor_doacao"],
                "data_doacao": doacao["data_doacao"].strftime("%d/%m/%Y"),
            }
        )

    context = {
        "usuario": usuario,
        "ultimas_doacoes": ultimas_doacoes,
        "total_doacoes": total_doacoes,
        "qtd_doacoes": qtd_doacoes,
    }

    return render(request, "meu_perfil.html", context)


@login_required
def expired_screen(request):
    """Exibe uma tela final com um conselho gerado pela API externa AdviceSlip."""
    URL_API = "https://api.adviceslip.com/advice"
    api = AdviceAPI(URL_API)
    advice = api.get_advice()

    if advice:
        return render(request, "expired_screen.html", {"advice": advice})
    else:
        return HttpResponse("Erro ao obter conselho da API")
