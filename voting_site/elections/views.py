from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, AdminUserAddForm, NomineeForm
from .models import Nominee, Vote, CustomUser


def footerpage(request):
    return render(request, "footer.html")
def aboutus(request):
    return render(request, "aboutus.html")

def landingpage(request):
    return render(request, "landing.html")

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Assuming 'login' is the name of your login URL
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        election_id = request.POST['election_id']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.election_id == election_id:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def nominees(request):
    nominees = Nominee.objects.filter(election_id=request.user.election_id)
    message = "No nominees found for your election ID." if not nominees else None
    return render(request, 'nominees.html', {'nominees': nominees, 'message': message})

# cast_vote view
@login_required
def cast_vote(request):
    nominees = Nominee.objects.filter(election_id=request.user.election_id)
    message = "You have already voted in this election. Go back and wait till the  election results." if Vote.objects.filter(user=request.user, election_id=request.user.election_id).exists() else None
    
    if request.method == 'POST':
        nominee_id = request.POST.get('nominee_id')
        nominee = Nominee.objects.get(id=nominee_id)
        Vote.objects.create(user=request.user, nominee=nominee, election_id=request.user.election_id)
        return redirect('results')
    
    return render(request, 'cast_vote.html', {'nominees': nominees, 'message': message})


@login_required
def results(request):
    nominees = Nominee.objects.filter(election_id=request.user.election_id)
    if not nominees.exists():
        message = "No results available for your election ID."
        return render(request, 'results.html', {'message': message, 'results': [], 'nominees': []})

    votes = Vote.objects.filter(election_id=request.user.election_id)
    if not votes.exists():
        message = "No votes recorded for your election ID."
        return render(request, 'results.html', {'message': message, 'results': [], 'nominees': []})

    results_data = {nominee: votes.filter(nominee=nominee).count() for nominee in nominees}
    total_votes = sum(results_data.values())
    results_percentage = [
        {'nominee': nominee, 'percentage': (count / total_votes) * 100 if total_votes else 0}
        for nominee, count in results_data.items()
    ]
    sorted_nominees = sorted(results_percentage, key=lambda x: x['percentage'], reverse=True)

    max_percentage = sorted_nominees[0]['percentage'] if sorted_nominees else 0
    winners = [item['nominee'] for item in sorted_nominees if item['percentage'] == max_percentage]

    for item in sorted_nominees:
        item['nominee'].vote_percentage = item['percentage']
        item['nominee'].is_winner = item['nominee'] in winners

    return render(request, 'results.html', {
        'results': sorted_nominees,
        'winners': winners,
        'tie': len(winners) > 1,
        'nominees': sorted_nominees
    })





@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    users = CustomUser.objects.all()
    return render(request, ' admin_dashboard.html', {'users': users})

@login_required
def add_nominee(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = NomineeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = NomineeForm()
    return render(request, ' add_nominee.html', {'form': form})

@login_required
def add_user(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = AdminUserAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = AdminUserAddForm()
    return render(request, ' add_user.html', {'form': form})
