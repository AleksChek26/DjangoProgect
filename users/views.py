import logging
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .forms import RegistrationForm, LoginForm, ProfileEditForm
from .models import CustomUser

logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)

            try:
                send_mail(
                    "Welcome to Our Site!",
                    f"Hello {user.email},\n\nThank you for registering!",
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, "Registration successful! Check your email.")
            except Exception as e:
                logger.error(f"Email sending failed: {e}")
                messages.warning(
                    request, "Registration successful, but email not sent."
                )

            return redirect("catalog:product_list")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("catalog:product_list")
            else:
                logger.warning(
                    f"Failed login attempt for email: {form.cleaned_data['username']}"
                )
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из аккаунта.")
    return redirect("catalog:product_list")


@login_required
@require_http_methods(["GET", "POST"])
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Ваш аккаунт успешно удалён.")
        return redirect("catalog:product_list")
    return render(request, "users/delete_account.html")


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect("users:edit_profile")
        else:
            messages.error(request, "Invalid data. Please check the fields.")
    else:
        form = ProfileEditForm(instance=user)
    return render(request, "users/edit_profile.html", {"form": form})
