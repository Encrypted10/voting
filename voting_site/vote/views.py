from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Nominee, Vote
from .forms import UserRegistrationForm, NomineeForm
from django.db.models import Count

def home(request):
    return render(request, 'vote/home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'vote/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'vote/register.html', {'form': form})

@login_required
def nominees(request):
    nominees = Nominee.objects.all()
    return render(request, 'vote/nominees.html', {'nominees': nominees})

@login_required
def cast_vote(request):
    if request.method == 'POST':
        nominee_id = request.POST.get('nominee')
        nominee = Nominee.objects.get(id=nominee_id)
        Vote.objects.create(user=request.user, nominee=nominee)
        return redirect('results')
    nominees = Nominee.objects.all()
    return render(request, 'vote/cast_vote.html', {'nominees': nominees})

@login_required
def results(request):
    nominees = Nominee.objects.annotate(vote_count=Count('vote')).order_by('-vote_count')
    total_votes = Vote.objects.count()
    return render(request, 'vote/results.html', {'nominees': nominees, 'total_votes': total_votes})

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
    return render(request, 'vote/admin_login.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        if 'add_nominee' in request.POST:
            nominee_form = NomineeForm(request.POST)
            if nominee_form.is_valid():
                nominee_form.save()
        elif 'add_user' in request.POST:
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
        return redirect('admin_dashboard')
    else:
        nominee_form = NomineeForm()
        user_form = UserRegistrationForm()
    users = User.objects.all()
    nominees = Nominee.objects.all()
    return render(request, 'vote/admin_dashboard.html', {
        'nominee_form': nominee_form, 
        'user_form': user_form, 
        'users': users, 
        'nominees': nominees
    })
