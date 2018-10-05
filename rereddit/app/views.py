from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Thread
from . import forms

# Create your views here.


def index(request):
    return render(request, "index.html")


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            return redirect('/index/')
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        # repeated login does not allowed
        if request.session.get('is_login', None):
            return redirect('/index/')

        if form.is_valid():
            # Log the user in
            user = form.get_user()

            # set session
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.username

            # login
            login(request, user)
            return redirect('/index/')
        else:
            return redirect('/index/')


def logout_view(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")

    logout(request)
    request.session.flush()
    return redirect("/index/")



def thread_list(request):
    threads = Thread.objects.all().order_by('created_date')
    return render(request, 'thread_list.html',{'threads': threads })


def thread_detail(request, id):
    thread = Thread.objects.get(id=id)
    return render(request, 'thread_detail.html', {'thread':thread})
    #return HttpResponse(title)


@login_required(login_url='/login/')
def thread_create(request):
    if request.method == 'POST':
        form = forms.CreateThread(request.POST, request.FILES)
        if form.is_valid():
            #save thread to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('/threads/')
    else:
        form = forms.CreateThread()
    return render(request, 'thread_create.html', {'form': form })


def search_result(request):
    content = request.GET.get('searchbox')
    threads = Thread.objects.filter(title__icontains=content)
    # print(content)
    return render(request, "result.html", {'threads': threads })
