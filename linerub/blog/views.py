# Create your views here.
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django import forms
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from blog.forms import UserForm, SubmitForm, HighlightForm
from blog.models import Share, Highlight
import heapq


def home(request):
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("home.html", {"user": request.user})


def dashboard(request):
    story = Share.objects.filter(publish = True).order_by("-id")
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("dashboard.html", {"user": request.user, "story": story})


def view(request):
    story = Share.objects.filter(user = request.user).order_by("-id")
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("view.html", {"user": request.user, "story": story})


def create(request):
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("create.html", {"user": request.user})


def profile(request, username):
    story = Share.objects.filter(user__username=username, publish = True).order_by("-id")
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("profile.html", {"user": request.user, "story": story})


def highlight(request):
    if request.method == 'POST':
        form = HighlightForm(request.POST)
        if form.is_valid():
            high = form.cleaned_data['highlight']
            story = Share.objects.filter(user = request.user, publish = False).order_by('-pk')[0]
            story.publish = True
            light = Highlight.objects.create(user = request.user, highlights = high, story = story)
            light.save()
            story.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = HighlightForm()
    return render_to_response("error.html", {"form": form})


def highlightw(request, id):
    if request.method == 'POST':
        form = HighlightForm(request.POST)
        if form.is_valid():
            high = form.cleaned_data['highlight']
            story = Share.objects.get(id = id)
            story.publish = True
            light = Highlight.objects.create(user = request.user, highlights = high, story = story)
            light.save()
            story.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = HighlightForm()
    return render_to_response("error.html", {"form": form})


def next(request):
    heap = []
    total = 0
    heap_large = []
    total_large = 0

    if (Share.objects.filter(user = request.user, publish = False).count() > 0):
        story = Share.objects.filter(user = request.user, publish = False).order_by('-pk')[0]
        cool = str(story.title)
        cooler = str(story.paragraph)
        trim = cool.split()
        trimmer = cooler.split()

        for w in trim:
            total = total + 1
            heapq.heappush(heap, (w, total))

        for word in trimmer:
            total_large = total_large + 1
            heapq.heappush(heap_large, (word, total_large))
    
        sortme = sorted(heap, key=lambda x: x[1])

        sortme_large = sorted(heap_large, key=lambda x: x[1])

        if not request.user.is_authenticated():
            return render_to_response("register.html")
    else:
        sortme = None
        sortme_large = None
    return render_to_response("step2.html", {"user": request.user, "title": sortme, "paragraph": sortme_large})


def nextw(request, id):
    heap = []
    total = 0
    heap_large = []
    total_large = 0

    if (Share.objects.filter(id = id, publish = False).count() > 0):
        story = Share.objects.get(id = id)
        cool = str(story.title)
        cooler = str(story.paragraph)
        trim = cool.split()
        trimmer = cooler.split()

        for w in trim:
            total = total + 1
            heapq.heappush(heap, (w, total))

        for word in trimmer:
            total_large = total_large + 1
            heapq.heappush(heap_large, (word, total_large))
    
        sortme = sorted(heap, key=lambda x: x[1])

        sortme_large = sorted(heap_large, key=lambda x: x[1])

        if not request.user.is_authenticated():
            return render_to_response("register.html")
    else:
        sortme = None
        sortme_large = None
    return render_to_response("step2_re.html", {"user": request.user, "title": sortme, "paragraph": sortme_large, "id": id})


def submit(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            tit = form.cleaned_data['title']
            para = form.cleaned_data['paragraph']
            story = Share.objects.create(user = request.user, title = tit, paragraph = para, publish = False)
            story.save()
            return HttpResponseRedirect('/next/')
    else:
        form = SubmitForm()
    return render_to_response("error.html", {"form": form})


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            newuser = User.objects.create_user(name, form.cleaned_data['email'], pw)
            newuser.save()
            user = authenticate(username = name, password = pw)
            auth_login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
    return render_to_response("register.html", {"form": form})


def login(request):
    username = password = ''
    error = False
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
  
        user = authenticate(username = username, password = password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            error = True
    return render_to_response("login.html", {"error": error})
  

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
