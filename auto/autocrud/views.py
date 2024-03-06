from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from autocrud.models import Auto, Make

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        nome = request.user.username
        return render(request, 'home.html', {'logado': True, 'user': nome})
    else:
        return render(request, 'home.html')
    
def cadastro(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Já existe um usuário com esse username')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save
        cadastrado = True
        return redirect('home')
    else:
        return render(request, 'cadastro.html')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login_django(request, user)
            return redirect('autocrud:autos')
        else:
            return HttpResponse('Usuário ou senha inválidos')

@login_required(login_url='/crud/login/') #Faz a autenticação e a gente escolhe a página de login (Por padrão é '/accounts/login/')
def autos(request):
    # if request.user.is_authenticated:
    if request.method == 'POST' and 'sair' in request.POST:
        logout(request)
        return redirect('autocrud:autos')
    else:
        user_id = request.user.id
        makeCount = Make.objects.filter(user_id=user_id).count()
        makes = Make.objects.filter(user_id=user_id)
        autos = Auto.objects.filter(user_id=user_id)
        return render(request, 'autolist.html', {'makeCount': makeCount, 'makes': makes, 'autos': autos })
    # else:
    #   return redirect('login')

@login_required(login_url='/crud/login/')
def makes(request):
    if request.method == 'POST' and 'sair' in request.POST:
        logout(request)
        return redirect('autocrud:autos')
    else:
        user_id = request.user.id
        makes = Make.objects.filter(user_id=user_id)
        autoCount = Auto.objects.filter(user_id=user_id).count()
        return render(request, 'makelist.html', {'makes': makes, 'autoCount': autoCount })

@login_required(login_url='/crud/login/')
def auto_create(request):
    if request.method == 'GET':
        return redirect('autocrud:autos')
    else:
        nickname = request.POST.get('name')
        mileage = request.POST.get('mileage')
        make_id = request.POST.get('make')
        user_id = request.user.id
        auto = Auto(nickname=nickname, mileage=mileage, user_id=user_id, make_id=make_id)
        auto.save()
    return redirect('autocrud:autos')

@login_required(login_url='/crud/login/')
def auto_update(request, autoid):
    if request.method == 'GET':
        try:
            auto = Auto.objects.get(id=autoid)
        except:
            return HttpResponse("Esse carro não existe")
        user_id = request.user.id
        if verifica(auto.user_id, user_id):
            user_id = request.user.id
            makeCount = Make.objects.filter(user_id=user_id).count()
            makes = Make.objects.filter(user_id=user_id)
            autos = Auto.objects.filter(user_id=user_id)
            return render(request, 'updateauto.html', {'makeCount': makeCount, 'makes': makes, 'autos': autos, 'autoId': autoid, 'auto': auto})
        else:
            return HttpResponse('Você não pode editar esse carro')
    else:
        auto = Auto.objects.get(id=autoid)
        auto.nickname = request.POST.get('name')
        auto.mileage = request.POST.get('mileage')
        auto.make_id = request.POST.get('make')
        auto.save()
        return redirect('autocrud:autos')

@login_required(login_url='/crud/login/')
def auto_delete(request, autoid): 
    try:
        auto = Auto.objects.get(id=autoid)
    except:
        return HttpResponse("Esse carro não existe")
    if verifica(auto.user_id, request.user.id):
        auto.delete()
    else:
        return HttpResponse('Você não pode deletar esse carro')
    return redirect('autocrud:autos')

@login_required(login_url='/crud/login/')
def make_create(request):
    if request.method == 'GET':
        return redirect('autocrud:makes')
    else:
        nome = request.POST.get('name')
        user_id = request.user.id
        if len(nome) > 2:
            make = Make(name=nome, user_id=user_id)
            make.save()
        else:
            return HttpResponse('Your make must be greater than 2 characters')
    if 'auto' in request.POST:
        return redirect('autocrud:autos')
    else:
        return redirect('autocrud:makes')

@login_required(login_url='/crud/login/')
def make_update(request, makeid):
    if request.method == 'GET':
        try:
            make = Make.objects.get(id=makeid)
            if verifica(make.user_id, request.user.id):
                makes = Make.objects.filter(user_id=request.user.id)
                autoCount = Auto.objects.filter(user_id=request.user.id).count()
                return render(request, 'updatemake.html', {'make': make, 'makes': makes, 'autoCount': autoCount })
            else:
                return HttpResponse("Você não pode editar essa marca")
        except:
            return HttpResponse("Essa marca não existe")
    else:
        make = get_object_or_404(Make, id=makeid)
        newName = request.POST.get('name')
        make.name = newName
        make.save()
        return redirect('autocrud:makes')

@login_required(login_url='/crud/login/')
def make_delete(request, makeid):
    try:
        make = Make.objects.get(id=makeid)
    except:
        return HttpResponse("Essa marca não existe")
    if verifica(make.user_id, request.user.id):
        make.delete()
        return redirect('autocrud:makes')
    else:
        return HttpResponse("Você não pode deletar essa marca")

def verifica(objUserId, userId):
    if objUserId == userId:
        return True
    else:
        return False