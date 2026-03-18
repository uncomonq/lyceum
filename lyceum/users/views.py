import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView

from .forms import ProfileForm, SignUpForm
from .models import Profile

User = get_user_model()

_ACTIVATION_TTL = datetime.timedelta(hours=12)


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("users:login")
    template_name = "users/signup.html"

    @transaction.atomic
    def form_valid(self, form):
        form.instance.is_active = settings.DEFAULT_USER_IS_ACTIVE
        response = super().form_valid(form)
        Profile.objects.get_or_create(user=self.object)
        self._send_activation_email(self.object.username)
        return response

    def _send_activation_email(self, username):
        activation_url = self.request.build_absolute_uri(
            reverse("users:activate", kwargs={"username": username}),
        )
        send_mail(
            subject="Активация аккаунта",
            message=(
                "Для активации аккаунта перейдите по ссылке:\n"
                f"{activation_url}\n"
                "Ссылка действует 12 часов."
            ),
            from_email=settings.DJANGO_MAIL,
            recipient_list=[self.object.email or settings.DJANGO_MAIL],
            fail_silently=True,
        )


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        users = list(User.objects.filter(is_active=True))
        for user in users:
            Profile.objects.get_or_create(user=user)

        return users


class UserDetailView(DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user_obj"

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        Profile.objects.get_or_create(user=user)
        return user


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile_obj,
            user=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён")
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=profile_obj, user=request.user)

    return render(
        request,
        "users/profile.html",
        {
            "form": form,
            "profile_obj": profile_obj,
        },
    )


def activate(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_active:
        messages.info(request, "Аккаунт уже активирован")
        return redirect("users:login")

    if timezone.now() - user.date_joined > _ACTIVATION_TTL:
        messages.error(request, "Срок действия ссылки активации истёк")
        return redirect("users:login")

    user.is_active = True
    user.save(update_fields=["is_active"])
    messages.success(request, "Аккаунт успешно активирован")
    return redirect("users:login")
