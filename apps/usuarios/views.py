from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

def cadastro(request):
    """Cadastra uma nova pessoa no sistema """
    if request.method == 'POST':
        nome = request.POST['nome'] #pega o nome do forms
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome): #se o campo está em branco
            messages.error(request, 'O nome não pode ficar em branco')
            print('O nome não pode ficar em branco')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'O email não pode ficar em branco')
            print('O email não pode ficar em branco')
            return redirect('cadastro')
        if senhas_diferentes(senha, senha2):
            messages.error(request, 'As senhas não são iguais')
            print('As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado')
            print('Usuário já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário já cadastrado')
            print('Usuário já cadastrado')
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        print('Usuário cadastrado com sucesso')
        messages.success(request, 'Usuário cadastrado com sucesso')
        subject = 'Bem vindo(a) ao Alura Receita'
        message = f'Olá {user.username}, obrigada por se cadastrar no Alura Receita.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list)
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    """Realiza o login do usuário no sistema """

    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if email == "" or senha == "":
            messages.error(request, 'Os campos email e senha não podem ficar em branco')
            print('Os campos email e senha não podem ficar em branco')
            return redirect('login')
        print(email, senha)
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso')
        return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def logout(request):
    """Faz o logout do usuário no sistema """

    auth.logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated: #entrar na page dashboard apenas se estiver logado
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        dados = {
            'receitas' : receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def campo_vazio(campo):
    return not campo.strip

def senhas_diferentes(senha, senha2):
    return senha != senha2