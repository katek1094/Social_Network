from django.shortcuts import render, redirect
from .forms import MyUserCreationForm
from app.models import UserProfile

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            UserProfile.objects.create(user=new_user)
            return redirect('login')
    else:
        form = MyUserCreationForm()
    return render(request, 'registration/signup.html', {"form": form})

