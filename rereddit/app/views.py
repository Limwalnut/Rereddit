from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Thread,Comment
from . import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import EditProfileForm
from django.contrib.auth import update_session_auth_hash

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
        return render(request, "account/signup.html")


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
    comments = Comment.objects.filter(threadID=thread)
    if request.method == "POST" and "reply_to_thread" in request.POST:
        print(request.POST['context'])
        print(request.user.username)
        comment_object = Comment(
            author=request.user,
            threadID=thread,
            text=request.POST['context']
        )
        comment_object.save()
    return render(request, 'thread_detail.html', {'thread': thread, 'comments': comments})
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


def profile_view(request):
    args = {'user':request.user}
    return render(request, "profile.html",args)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        # form = EditProfileForm(request.POST, instance= request.user)

        form = EditProfileForm(request.POST, request.FILES, instance=request.user, initial={
        'gender': user.profile.gender,
        'first_name':user.profile.first_name,
        'last_name':user.profile.last_name,
        'phone':user.profile.phone,
        'email':user.profile.email,
        'image':user.profile.image})
        if form.is_valid():
            user.profile.gender = request.POST['gender']
            user.profile.first_name = request.POST['first_name']
            user.profile.last_name = request.POST['last_name']
            user.profile.phone = request.POST['phone']
            user.profile.email = request.POST['email']
            user.profile.image = request.FILES['image']
            user.save()
            form.save()
            return redirect('/profile')

    else:
        form = EditProfileForm(instance=request.user)
        args= {'form':form}
        return render(request,'profile_update.html',args)


@login_required
def change_passwords(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile')
        else:
            return redirect('/change_password')

    else:
        form = PasswordChangeForm(user = request.user)
        args = {'form':form}
        return render(request, 'change_password.html',args)


