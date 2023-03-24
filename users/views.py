from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegister, UserUpdateForm, ProfileUpdateForm
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from genre.models import FavouriteMovie


def registration_user(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('signin')
    else:
        form = UserRegister()
    return render(request, "users/registration.html", {"form": form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated !')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    return render(request, 'users/profile.html', context)


def delete_user(request):
    del_fav = FavouriteMovie.objects.all()
    for item in del_fav:
        if item.user_id == request.user.id:
            item.delete()

    user = User.objects.get(id=request.user.id)
    user.delete()

    return redirect('signin')
