from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.defaulttags import register
from . import make_statistics
import datetime


@register.filter
def get_range(value):
    return range(value)

from .models import User, LearningSession

### Views

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'learning_marathon/login.html')
    if request.method == 'POST':

        if request.user.now_learning:
            current_session = LearningSession.objects.filter(user=request.user).last()
            current_session.end_date = datetime.datetime.now()
            current_session.save()
            request.user.now_learning = False
            request.user.theory = False
            request.user.save()
        else:
            if 'theory' in request.POST:
                current_session = LearningSession.objects.create(user = request.user, theory = True)
                request.user.theory = True
            else:
                current_session = LearningSession.objects.create(user = request.user, theory = False)
            current_session.save()
            request.user.now_learning = True
            request.user.save()
            return HttpResponseRedirect(reverse('learning_marathon:index'))

    return render(request, 'learning_marathon/index.html')

@login_required
def statistics(request):
    data = make_statistics.get_data(request.user)[:-1]
    summary = make_statistics.get_data(request.user)[-1]

    return render(request, 'learning_marathon/statistics.html', {'data':data,
                                                                'summary':summary})

def login_view(request):
    if request.method == "POST":

        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('learning_marathon:index'))
        else:
            return render (request,
                        'learning_marathon/login.html',
                        {'error_message': f'Invalid credentials :-('}
                    )

    return render(request, 'learning_marathon/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first-name']
        username = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        if password != confirmation:
            return render (request,
                        'learning_marathon/register.html',
                        {'error_message': 'Password must match!  :-('}
                    )

        new_user = User.objects.create_user(first_name = first_name, username = username, password = password)
        new_user.save()
        login(request, new_user)
        return render (request,
                        'learning_marathon/index.html',
                        {'success_message': 'Congratulations! Registration successful :-)'}
                    )

    return render(request, 'learning_marathon/register.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('learning_marathon:login'))