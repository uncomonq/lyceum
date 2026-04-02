__all__ = ()
import datetime

import django.conf
import django.contrib.auth.mixins
import django.contrib.auth.views
import django.contrib.messages
import django.core.mail
from django.db.models import Q
import django.shortcuts
import django.urls
import django.utils.timezone
from django.utils.translation import gettext_lazy as _
import django.views
import django.views.generic

import users.forms
import users.models


class LoginView(django.contrib.auth.views.LoginView):
    pass


class LogoutView(django.contrib.auth.views.LogoutView):
    http_method_names = ["post", "options"]


class PasswordChangeView(django.contrib.auth.views.PasswordChangeView):
    pass


class PasswordChangeDoneView(django.contrib.auth.views.PasswordChangeDoneView):
    pass


class PasswordResetView(django.contrib.auth.views.PasswordResetView):
    pass


class PasswordResetDoneView(django.contrib.auth.views.PasswordResetDoneView):
    pass


class PasswordResetConfirmView(
    django.contrib.auth.views.PasswordResetConfirmView,
):
    pass


class PasswordResetCompleteView(
    django.contrib.auth.views.PasswordResetCompleteView,
):
    pass


class SignUpView(django.views.generic.FormView):
    form_class = users.forms.UserCreationForm
    success_url = django.urls.reverse_lazy("users:login")
    template_name = "users/signup.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        user.is_staff = False
        user.is_superuser = False
        user.save()
        users.models.Profile.objects.get_or_create(user=user)

        activate_url = django.urls.reverse(
            "users:activate",
            kwargs={"username": user.username},
        )
        django.core.mail.send_mail(
            _("Hello %(username)s") % {"username": user.username},
            _("Follow the activation link: %(url)s") % {"url": activate_url},
            django.conf.settings.DJANGO_MAIL,
            [user.email or django.conf.settings.DJANGO_MAIL],
            fail_silently=False,
        )

        return super().form_valid(form)


class ActivateView(django.views.View):
    http_method_names = ["get", "options"]

    def get(self, request, username, *args, **kwargs):
        user = django.shortcuts.get_object_or_404(
            users.models.User,
            username=username,
        )
        if not user.is_active:
            activation_expired_at = user.date_joined + datetime.timedelta(
                hours=12,
            )
            if django.utils.timezone.now() <= activation_expired_at:
                user.is_active = True
                user.save(update_fields=["is_active"])

        return django.shortcuts.redirect(django.urls.reverse("users:login"))


class ReactivateView(django.views.View):
    http_method_names = ["get", "options"]

    def get(self, request, username, *args, **kwargs):
        user = django.shortcuts.get_object_or_404(
            users.models.User,
            username=username,
        )
        profile, _ = users.models.Profile.objects.get_or_create(user=user)
        if (
            not user.is_active
            and profile.blocked_at is not None
            and django.utils.timezone.now()
            <= profile.blocked_at + datetime.timedelta(weeks=1)
        ):
            user.is_active = True
            user.save(update_fields=["is_active"])
            profile.attempts_count = 0
            profile.blocked_at = None
            profile.save(update_fields=["attempts_count", "blocked_at"])

        return django.shortcuts.redirect(django.urls.reverse("users:login"))


class UserListView(django.views.generic.ListView):
    context_object_name = "users"
    queryset = users.models.User.objects.active()


class UserDetailView(django.views.generic.DetailView):
    context_object_name = "user_obj"

    def get_queryset(self):
        return users.models.User.objects.active()


class BirthdayUsersListView(django.views.generic.ListView):
    context_object_name = "users"
    template_name = "users/birthday_users.html"

    def get_queryset(self):
        today = django.utils.timezone.localdate()
        return (
            users.models.User.objects.active()
            .filter(
                ~Q(email=""),
                profile__birthday__month=today.month,
                profile__birthday__day=today.day,
            )
            .order_by("username")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Today's birthdays")
        return context


class ProfileView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    template_name = "users/profile.html"

    def _build_forms(self, request):
        profile, _ = users.models.Profile.objects.get_or_create(
            user=request.user,
        )
        user_form = users.forms.UserChangeForm(
            request.POST or None,
            instance=request.user,
        )
        profile_form = users.forms.UpdateProfileForm(
            request.POST or None,
            request.FILES or None,
            instance=profile,
        )

        return profile, user_form, profile_form

    def get(self, request, *args, **kwargs):
        profile, user_form, profile_form = self._build_forms(request)
        return django.shortcuts.render(
            request,
            self.template_name,
            {
                "profile_obj": profile,
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )

    def post(self, request, *args, **kwargs):
        profile, user_form, profile_form = self._build_forms(request)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            django.contrib.messages.success(request, _("Saved"))
            return django.shortcuts.redirect(
                django.urls.reverse("users:profile"),
            )

        return django.shortcuts.render(
            request,
            self.template_name,
            {
                "profile_obj": profile,
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )
