from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Hood, Location, Post, User, Business
from .forms import HoodForm, UserForm, MyUserCreationForm, BusinessForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user doesnt exist')

        user = authenticate(request, username= username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password does not exist')

    context = {
        'page':page
    }
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    page = 'register'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    context = {
        'form':form,
        'page':page
    }

    return render(request, 'login.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    hoods = Hood.objects.filter(Q(location__name__icontains=q) | Q(name__icontains=q))
    locations = Location.objects.all()
    hood_count = hoods.count()
    posts = Post.objects.filter(Q(hood__location__name__icontains=q))

    context = {
        'hoods':hoods,
        'locations':locations,
        'hood_count':hood_count, 
        'posts':posts
    }
    return render(request, 'home.html', context)


def hood(request, pk):
    hood = Hood.objects.get(id=pk)  
    posts = hood.post_set.all().order_by('-created')  
    occupants = hood.occupants.all()
    businesses = hood.biashara.all()

    if request.method == 'POST':
        post = Post.objects.create(
            user = request.user,
            hood = hood,
            body = request.POST.get('body')
        )
        
        return redirect('hood', pk=hood.id)
    context = {
        'hood':hood,
        'posts':posts, 
        'occupants':occupants,
        'businesses':businesses
    }
    return render(request, 'neighbourhood.html', context)


def joinHood(request,pk):
    hood = Hood.objects.get(id=pk)
    hood.occupants.add(request.user)
    occupants = hood.occupants.all()

    context = {
       'hood':hood,
       'occupants':occupants 
    }
    return render(request, 'neighbourhood.html', context)


def quitHood(request,pk):
    hood = Hood.objects.get(id=pk)
    hood.occupants.remove(request.user)
    posts = hood.post_set.all().order_by('-created')  
    occupants = hood.occupants.all()
    context = {
        'posts':posts,
        'occupants':occupants,
        'hood':hood
    }
    return render(request, 'home.html', context)


def userProfile(request , pk):
    user = User.objects.get(id=pk)
    hoods = user.hood_set.all()
    posts = user.post_set.all()
    locations = Location.objects.all()
    context = {
        'user':user,
        'hoods':hoods,
        'posts':posts,
        'locations':locations
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def createHood(request):
    form = HoodForm()
    if request.method == 'POST':
        form = HoodForm(request.POST)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.host = request.user
            hood.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'hood_form.html', context)

@login_required(login_url='login')
def createBusiness(request, pk):
    hood = Hood.objects.get(id=pk)
    form = BusinessForm()
    user = request.user

    
    if request.method == 'POST':
        business = Business.objects.create (
            owner = user,
            neighborhood = hood,
            name = request.POST.get('name'),
            email= request.POST.get('email'),
            contact = request.POST.get('contact'),

        )
        return redirect('hood', pk=hood.id)

       
    context = {
        'form':form,
        'hood': hood
    }
    return render(request, 'create_business.html', context)


@login_required(login_url='login')
def updateHood(request, pk):
    hood = Hood.objects.get(id=pk)
    form = HoodForm(instance=hood)

    if request.user != hood.host:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        form = HoodForm(request.POST, instance=hood)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form':form
    }
    return render(request, 'hood_form.html', context)



@login_required(login_url='login')
def deleteHood(request, pk):
    hood = Hood.objects.get(id=pk)

    if request.user != hood.host:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        hood.delete()
        return redirect('home')
    context = {

    }
    return render(request, 'delete.html', {'obj':hood})



@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)

    if request.user != post.user:
        return HttpResponse('You are not allowed')

    if request.method == 'POST':
        post.delete()
        return redirect('home')
    context = {

    }
    return render(request, 'delete.html', {'obj':post})



@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)

    context = {
        'form':form
    }
    return render(request, 'userUpdate.html', context)


