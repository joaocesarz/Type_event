from django.shortcuts import redirect, render
from django .http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from django.contrib import auth

def cadastro(request):
    match request.method:

        case "GET":
            return render(request, 'cadastro.html')
        
        case "POST":
            username = request.POST.get('username')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            confirmar_senha = request.POST.get('confirmar_senha')
               
            if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senhas não coincidem.')
            return redirect(reverse('cadastro')) 

            # TODO: validar força da senha

            user = User.objects.filter(username=username)

            if user.exists():
                messages.add_message(request, constants.ERROR, 'Usuário já existe.')
                return redirect(reverse('cadastro'))
            

            user = User.objects.create_user(username=username, email=email, password=senha)
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso.')
        
            return redirect(reverse('login'))

def login(request):
    match request.method:
        
        case 'GET':
            return render(request, 'login.html')
        
        case 'POST':
            username = request.POST.get('username')
            senha = request.POST.get('senha')

            user = auth.authenticate(username=username, password=senha)

            if not user:
                messages.add_message(request, constants.ERROR, 'Username ou senha inválidos.')
                return redirect(reverse('login'))
        
            auth.login(request, user)
            return redirect('/eventos/novo_evento/')
