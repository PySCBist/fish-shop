from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CreationForm


def signup(request):
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
            return redirect('index')
    else:
        form = CreationForm()
    return render(request, 'signup.html', {'form': form})
