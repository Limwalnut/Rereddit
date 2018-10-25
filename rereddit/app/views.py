from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Thread, Comment, User, Profile, Tag, FollowTag, File, ThreadFile,Friends
from . import forms
from .forms import EditProfileForm, UserCreateForm, UserForm
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
import os
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.


def index(request):
    threads = Thread.objects.all().order_by('created_date')
    if request.user.is_authenticated:
        try:
            tag=FollowTag.objects.get(current_user=request.user)
            tags = tag.tag.all()
            tag1 = Tag.objects.all()
            return render(request, "index.html", {'threads': threads, 'tag': tag, 'tags': tags, 'tag1': tag1})
        except ObjectDoesNotExist:
            tag = None
            return render(request, "index.html", {'threads': threads})

    else:
        return render(request, "index.html", {'threads': threads})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            return redirect('/index/')
        else:
            return render(request, 'account/error_info.html',
                          {'err_msg': 'create user failed, please check input data and try again!'})
    else:
        return render(request, "account/signup.html")


def login_view(request):
    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # repeated login does not allowed
            if request.session.get('is_login', None):
                return render(request, '/account/error_info.html',
                              {'err_msg': 'You cannot login twice!'})

            # Log the user in
            user = form.get_user()
            if user is not None:
                # set session
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username

                login(request, user)
                # Redirect to a success page.
                return redirect('/index/')
            else:
                return render(request, 'account/error_info.html',
                              {'err_msg': 'Invalid login: username or password is incorrect! please try again!'})
        else:
            # Return an 'invalid login' error message.
            return render(request, 'account/error_info.html',
                          {'err_msg': 'Invalid login: username or password is incorrect! please try again!'})
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
    threadFile = None
    threadFile = ThreadFile.objects.filter(threadId=thread)
    file=""
    if threadFile:
        file = threadFile.get(threadId=thread).fileId
    commentsToThread = Comment.objects.filter(threadID=thread,parentCommentID=None)
    commentsToComment = Comment.objects.filter(threadID=thread, parentCommentID__isnull=False)
    thisUser = request.user

    anonymous = False
    # check if thread is anonymous
    anon_tags = thread.tags.filter(name='#anonymous')


    if len(anon_tags) > 0:
        anonymous = True
        anonymous_user = Profile.objects.filter(user__username='Anonymous')

        # for the thread if the author
        # need to change the model for thread to Profile


        # comment author not equal to this user
        for i in commentsToThread:
            # if the author is not this user direct to anonymouse
            if i.author != Profile.objects.filter(user__username=thisUser.username):
                i.author = anonymous_user[0]

        for i in commentsToComment:
            # if the author is not this user direct to anonymouse
            if i.author != Profile.objects.filter(user__username=thisUser.username):
                i.author = anonymous_user[0]

    if request.method == "POST" and "reply_to_thread" in request.POST:
        print(request.POST['context'])
        print(request.user.username)
        comment_object = Comment(
            author=request.user.profile,
            threadID=thread,
            text=request.POST['context']
        )
        comment_object.save()

        # add hash tags if any
        # get tags
        hash_tags = []
        # add code to check for '#'
        text = request.POST['context']
        for i in text.split():
            if i[0] == '#':
                # append tag to an array
                hash_tags.append(i)

        for i in hash_tags:
            # find if tag exists
            t = Tag.objects.filter(name=i)
            if len(t) > 0:
                comment_object.tags.add(t.get())
            else:
                # add tag
                new_t = Tag(name=i)
                new_t.save()
                comment_object.tags.add(new_t)
        return redirect('/thread/'+str(thread.id)+'/redirect/')
    elif request.method == "POST" and "reply_to_comment" in request.POST:
        print(request.POST['context'])
        print(request.POST['parent'])
        # print(request.user.username)
        comment_object = Comment(
            author=request.user.profile,
            threadID=thread,
            parentCommentID=Comment.objects.get(id=request.POST['parent']),
            text=request.POST['context']
        )
        comment_object.save()

        # add hash tags if any
        # get tags
        hash_tags = []
        # add code to check for '#'
        text = request.POST['context']
        for i in text.split():
            if i[0] == '#':
                # append tag to an array
                hash_tags.append(i)

        for i in hash_tags:
            # find if tag exists
            t = Tag.objects.filter(name=i)
            if len(t) > 0:
                comment_object.tags.add(t.get())
            else:
                # add tag
                new_t = Tag(name=i)
                new_t.save()
                comment_object.tags.add(new_t)
        return redirect('/thread/' + str(thread.id) + '/redirect/')
    elif request.method == "POST" and "edit_comment" in request.POST:
        print("Editing a comment")
        print(request.POST['context'])
        print(request.POST['commId'])
        comment = Comment.objects.get(id=request.POST['commId'])
        comment.text = request.POST['context']
        comment.save()
        # add hash tags if any
        # get tags
        hash_tags = []
        # add code to check for '#'
        text = request.POST['context']
        for i in text.split():
            if i[0] == '#':
                # append tag to an array
                hash_tags.append(i)

        for i in hash_tags:
            # find if tag exists
            t = Tag.objects.filter(name=i)
            if len(t) > 0:
                comment_object.tags.add(t.get())
            else:
                # add tag
                new_t = Tag(name=i)
                new_t.save()
                comment_object.tags.add(new_t)
        return redirect('/thread/' + str(thread.id) + '/redirect/')
    elif request.method == "POST" and "edit_thread" in request.POST:
        print("Editing a thread")
        text = request.POST['context']
        thread.text = text
        thread.save()

        # get tags
        hash_tags = []
        # add code to check for '#'
        for i in text.split():
            if i[0] == '#':
                # append tag to an array
                hash_tags.append(i)

        for i in hash_tags:
            # find if tag exists
            t = Tag.objects.filter(name=i)
            if len(t) > 0:
                thread.tags.add(t.get())
            else:
                # add tag
                new_t = Tag(name=i)
                new_t.save()
                thread.tags.add(new_t)
    elif request.is_ajax():
        commentID = request.POST['commentID']
        Comment.objects.get(id=commentID).delete()

    return render(request, 'thread_detail.html',
                  {'thread': thread,
                   'commentsToThread': commentsToThread,
                   'commentsToComment': commentsToComment,
                   'file': file,
                   'thisUser': thisUser})
    #return HttpResponse(title)


def file_download(request, id):
    threadfile = ThreadFile.objects.get(threadId=id)
    file_path = threadfile.fileId.filePath

    def file_iterator(file_name, chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + threadfile.fileId.name

    return response


@login_required(login_url='/login/')
def thread_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        user = request.user
        # create new thread
        thread = Thread(title=title, text=text, author=user)
        thread.save()

        myFile = request.FILES.get("myfile", None)
        if myFile:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            BASE_DIR2 = os.path.join(BASE_DIR, 'media')
            BASE_DIR3 = os.path.join(BASE_DIR2, 'media')
            BASE_DIR4 = os.path.join(BASE_DIR3, 'uploads')
            FILE_DIR = os.path.join(BASE_DIR4, myFile.name)
            destination = open(FILE_DIR, 'wb+')
            for chunk in myFile.chunks():
                destination.write(chunk)
            destination.close()

            file_object = File(name=myFile.name, filePath=FILE_DIR)
            file_object.save()

            thread_file = ThreadFile(threadId=thread, fileId=file_object)
            thread_file.save()

        # get tags
        hash_tags = []
        # add code to check for '#'
        for i in text.split():
            if i[0] == '#':
                # append tag to an array
                hash_tags.append(i)

        for i in hash_tags:
            # find if tag exists
            t = Tag.objects.filter(name=i)
            if len(t) > 0:
                thread.tags.add(t.get())
            else:
                # add tag
                new_t = Tag(name=i)
                new_t.save()
                thread.tags.add(new_t)

        return redirect('/threads/')
    else:
        form = forms.CreateThread()
    return render(request, 'thread_create.html', {'form': form })

@csrf_exempt
def search_result(request):
    content = request.GET.get('searchbox')
    threads = Thread.objects.filter(tags__name__contains=content)

    if request.user.is_authenticated:
        try:
            tag = FollowTag.objects.get(current_user=request.user)
            try:
                search_tag = Tag.objects.get(name = "#"+content)
                tags = tag.tag.all()
                return render(request, "result.html", {'threads': threads, 'tag':tag, 'tags':tags,'search_tag':search_tag })
            except ObjectDoesNotExist:
                return render(request, 'account/error_info.html',
                              {'err_msg': 'This tag has not been created!'})

        except ObjectDoesNotExist:
            try:
                search_tag = Tag.objects.get(name="#" +content)
                return render(request, "result.html",{'threads': threads, 'search_tag': search_tag})
            except ObjectDoesNotExist:
                return render(request, 'account/error_info.html',
                              {'err_msg': 'This tag has not been created!'})
    else:
        return render(request, "result.html", {'threads': threads})



def profile_view(request, id):
    # args = {'user':request.user}
    thisUser = request.user
    user = User.objects.get(id=id)
    # args = {'user': User.objects.get(id=id),'thisUser':thisUser}
    # return render(request, "account/profile.html",args)

    if request.user.is_authenticated:
        try:
            friends = Friends.objects.get(current_user=request.user)
            friend = friends.friend.all()
            return render(request, "account/profile.html", {'friends': friends, 'friend': friend,'thisUser':thisUser,'user':user})
        except ObjectDoesNotExist:
            friends = None
            return render(request, "account/profile.html", {'friends': friends,'thisUser':thisUser,'user':user})

    else:
        return render(request, "account/profile.html",{'thisUser':thisUser,'user':user})


@login_required
@transaction.atomic
def edit_profile(request, id):
    if request.method == 'POST':
        user_object = User.objects.get(pk=id)
        profile_object = Profile.objects.get(user=user_object)
        user_form = UserForm(request.POST, instance = user_object)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile_object)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/profile/'+id)

    else:
        user_object = User.objects.get(pk=id)
        profile_object = Profile.objects.get(user=user_object)
        user_form = UserForm(instance = user_object)
        profile_form = EditProfileForm(instance=profile_object)
        return render(request,'account/profile_update.html',{
            'user_form':user_form,
            'profile_form': profile_form
        })



@login_required
def change_passwords(request, id):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user )

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile/'+id)
        else:
            return redirect('/profile/'+id+'/change_password/')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'account/change_password.html',args)


def search_tag(request,name):
    content = name
    threads = Thread.objects.filter(tags__name__contains=content)
    if request.user.is_authenticated:
        try:
            tag = FollowTag.objects.get(current_user=request.user)
            search_tag = Tag.objects.get(name="#" + content)
            tags = tag.tag.all()
            return render(request, "result.html",
                          {'threads': threads, 'tag': tag, 'tags': tags, 'search_tag': search_tag})
        except ObjectDoesNotExist:
            search_tag = Tag.objects.get(name="#" + content)
            return render(request, "result.html", {'threads': threads, 'search_tag': search_tag})


    else:
        return render(request, "result.html", {'threads': threads})

def subscribeTags(request, operation, id):
    new_tag = Tag.objects.get(id =id)
    if operation == 'add':
        FollowTag.subscribe_tag(request.user, new_tag)
    else:
        FollowTag.unsubscribe_tag(request.user, new_tag)
    return  redirect('/index/')

def redirectPage(request, id):
    # return redirect('/'+id+'/')
    return render(request, "redirect.html", {'threadID': id})

def friend_list(request):
    # friends = Friends.objects.get(current_user = request.user)
    if request.user.is_authenticated:
        try:
            friends = Friends.objects.get(current_user=request.user)
            friend = friends.friend.all()
            return render(request, "account/friend_list.html", {'friends': friends,'friend':friend})
        except ObjectDoesNotExist:
            friends = None
            return render(request, "account/friend_list.html", {'friends': friends})

    else:
        return render(request, "account/friend_list.html")

def follow_friend(request, operation, id):
    new_friend = User.objects.get(id=id)
    if operation == 'add':
        Friends.subscribe_friend(request.user, new_friend)
    else:
        Friends.unsubscribe_friend(request.user, new_friend)
    return redirect('/friend_list/')





