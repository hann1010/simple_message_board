from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('chat-home')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'register'
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES, # For Profile Pic
                                    instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('chat-home')

    else:
        user_level_int = request.user.profile.user_level
        if user_level_int > 4:
            user_level_tmp = 'Post, update, comments and delete'
        elif user_level_int > 3:
            user_level_tmp = 'Post, update and comments'
        else:
            user_level_tmp = 'Read only'
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'form': u_form,
        'p_form': p_form,
        'title': 'profile',
        'user_level': user_level_tmp
    }
    return render(request, 'users/profile.html', context)

