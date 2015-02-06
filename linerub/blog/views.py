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
from blog.forms import UserForm, SubmitForm, HighlightForm, TagForm
from blog.models import Share, Highlight, Link
import heapq


def home(request):
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("home.html", {"user": request.user})


def exchange(request):

    array = []
    array_large = []
    total = 0
    total_large = 0

    story = Share.objects.filter(publish = True).order_by("?")[:1]
    tags = Link.objects.all()

    for s in story:

        link = Link.objects.filter(story = s)

        cool = str(s.title)
        cooler = str(s.paragraph)
        trim = cool.split()
        trimmer = cooler.split()

        for w in trim:
            flag = False
            for l in link:
                if w == l.links:
                    heapq.heappush(array, (l, total, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array, (w, total, s.id))
            total = total + 1

        for word in trimmer:
            flag = False
            for l in link:
                if word == l.links:
                    heapq.heappush(array_large, (l, total_large, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array_large, (word, total_large, s.id))
            total_large = total_large + 1

    sortme = sorted(array, key=lambda x: x[1])
    sortme_large = sorted(array_large, key=lambda x: x[1])

    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("exchange.html", {"user": request.user, "snippet": sortme, "snippet_large": sortme_large, "story": story, "links": tags})


def tag(request, id, word):
    if request.method == 'POST':
        form = TagForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            story = Share.objects.get(id = id)
            links = Link.objects.get(story = story, links = word) 
            links.path = image
            links.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = TagForm()
    return render_to_response("dashboard.html", {"form": form})
    

# Changes made
def dashboard(request):

    array = []
    array_large = []
    total = 0
    total_large = 0

    story = Share.objects.filter(publish = True).order_by("-id")
    tags = Link.objects.all()

    for s in story:

        link = Link.objects.filter(story = s)

        cool = str(s.title)
        cooler = str(s.paragraph)
        trim = cool.split()
        trimmer = cooler.split()

        for w in trim:
            flag = False
            for l in link:
                if w == l.links:
                    heapq.heappush(array, (l, total, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array, (w, total, s.id))
            total = total + 1

        for word in trimmer:
            flag = False
            for l in link:
                if word == l.links:
                    heapq.heappush(array_large, (l, total_large, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array_large, (word, total_large, s.id))
            total_large = total_large + 1

    sortme = sorted(array, key=lambda x: x[1])
    sortme_large = sorted(array_large, key=lambda x: x[1])

    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("dashboard.html", {"user": request.user, "snippet": sortme, "snippet_large": sortme_large, "story": story, "links": tags})


def view(request):
    array = []
    array_large = []
    total = 0
    total_large = 0

    story = Share.objects.filter(user = request.user).order_by("-id")
    tags = Link.objects.all()

    for s in story:

        link = Link.objects.filter(story = s)

        cool = str(s.title)
        cooler = str(s.paragraph)
        trim = cool.split()
        trimmer = cooler.split()

        for w in trim:
            flag = False
            for l in link:
                if w == l.links:
                    heapq.heappush(array, (l, total, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array, (w, total, s.id))
            total = total + 1

        for word in trimmer:
            flag = False
            for l in link:
                if word == l.links:
                    heapq.heappush(array_large, (l, total_large, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array_large, (word, total_large, s.id))
            total_large = total_large + 1

    sortme = sorted(array, key=lambda x: x[1])
    sortme_large = sorted(array_large, key=lambda x: x[1])

    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("view.html", {"user": request.user, "snippet": sortme, "snippet_large": sortme_large, "story": story, "links": tags})


def create(request):
    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("create.html", {"user": request.user})


def profile(request, username):

    array = []
    array_large = []
    total = 0
    total_large = 0

    story = Share.objects.filter(user__username=username, publish = True).order_by("-id")
    tags = Link.objects.all()

    for s in story:

        link = Link.objects.filter(story = s)

        cool = str(s.title)
        cooler = str(s.paragraph)
        trim = cool.split()
        trimmer = cooler.split()

        for w in trim:
            flag = False
            for l in link:
                if w == l.links:
                    heapq.heappush(array, (l, total, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array, (w, total, s.id))
            total = total + 1

        for word in trimmer:
            flag = False
            for l in link:
                if word == l.links:
                    heapq.heappush(array_large, (l, total_large, s.id))
                    flag = True
            if (flag == False):
                heapq.heappush(array_large, (word, total_large, s.id))
            total_large = total_large + 1

    sortme = sorted(array, key=lambda x: x[1])
    sortme_large = sorted(array_large, key=lambda x: x[1])

    if not request.user.is_authenticated():
        return render_to_response("register.html")
    return render_to_response("profile.html", {"user": request.user, "snippet": sortme, "snippet_large": sortme_large, "story": story, "links": tags})


def highlight(request):
    if request.method == 'POST':
        form = HighlightForm(request.POST)
        if form.is_valid():
            high = form.cleaned_data['highlight']
            tag = form.cleaned_data['tag']
            story = Share.objects.filter(user = request.user, publish = False).order_by('-pk')[0]
            story.publish = True
            light = Highlight.objects.create(user = request.user, highlights = high, tags = tag, story = story)
            light.save()
            story.save()

            cool = str(light.highlights)
            cooler = str(story.paragraph)
            coolest = str(story.title)
            trim = cool.split()
            trimmer = cooler.split()
            trimmest = coolest.split()

            for word in trimmer:
                for w in trim:
                    if (word == w):
                        if (Link.objects.filter(links = word, story = story).count() == 0):
                            link = Link.objects.create(links = word, story = story, path = None)

            for words in trimmest:
                for w in trim:
                    if (words == w):
                        if (Link.objects.filter(links = words, story = story).count() == 0):
                            link = Link.objects.create(links = words, story = story, path = None)

            return HttpResponseRedirect('/dashboard/')
    else:
        form = HighlightForm()
    return render_to_response("error.html", {"form": form})


def highlightw(request, id):
    if request.method == 'POST':
        form = HighlightForm(request.POST)
        if form.is_valid():
            high = form.cleaned_data['highlight']
            tag = form.cleaned_data['tag']
            story = Share.objects.filter(user = request.user, publish = False).order_by('-pk')[0]
            story.publish = True
            light = Highlight.objects.create(user = request.user, highlights = high, tags = tag, story = story)
            light.save()
            story.save()

            cool = str(light.highlights)
            cooler = str(story.paragraph)
            coolest = str(story.title)
            trim = cool.split()
            trimmer = cooler.split()
            trimmest = coolest.split()

            for word in trimmer:
                for w in trim:
                    if (word == w):
                        if (Link.objects.filter(links = word, story = story).count() == 0):
                            link = Link.objects.create(links = word, story = story, path = None)

            for words in trimmest:
                for w in trim:
                    if (words == w):
                        if (Link.objects.filter(links = words, story = story).count() == 0):
                            link = Link.objects.create(links = words, story = story, path = None)

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
