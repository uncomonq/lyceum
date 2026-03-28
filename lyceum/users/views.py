__all__ = ()
import datetime

import django.conf
import django.contrib.auth.mixins
import django.contrib.auth.views
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.urls
import django.utils.timezone
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
            f"Здравствуй {user.username}",
            "Перейди по ссылке для активации аккаунта " f"{activate_url}",
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


class ProfileView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    template_name = "users/profile.html"

    def get_profile(self):
        profile, _ = users.models.Profile.objects.get_or_create(
            user=self.request.user,
        )
        return profile

    def get_user_form(self):
        kwargs = {"instance": self.request.user}
        if self.request.method == "POST":
            kwargs["data"] = self.request.POST

        return users.forms.UserChangeForm(**kwargs)

    def get_profile_form(self, profile):
        kwargs = {"instance": profile}
        if self.request.method == "POST":
            kwargs["data"] = self.request.POST
            kwargs["files"] = self.request.FILES

        return users.forms.UpdateProfileForm(**kwargs)

    def get_context_data(self, **kwargs):
        return {
            "profile_obj": kwargs["profile"],
            "user_form": kwargs["user_form"],
            "profile_form": kwargs["profile_form"],
        }

    def render_to_response(self, context):
        return django.shortcuts.render(
            request=self.request,
            template_name=self.template_name,
            context=context,
        )

    def forms_valid(self, user_form, profile_form):
        user_form.save()
        profile_form.save()
        django.contrib.messages.success(self.request, "Сохранено")
        return django.shortcuts.redirect(django.urls.reverse("users:profile"))

    def forms_invalid(self, profile, user_form, profile_form):
        return self.render_to_response(
            self.get_context_data(
                profile=profile,
                user_form=user_form,
                profile_form=profile_form,
            ),
        )

    def get(self, request, *args, **kwargs):
        profile = self.get_profile()
        return self.render_to_response(
            self.get_context_data(
                profile=profile,
                user_form=self.get_user_form(),
                profile_form=self.get_profile_form(profile),
            ),
        )

    def post(self, request, *args, **kwargs):
        profile = self.get_profile()
        user_form = self.get_user_form()
        profile_form = self.get_profile_form(profile)
        if user_form.is_valid() and profile_form.is_valid():
            return self.forms_valid(user_form, profile_form)

        return self.forms_invalid(profile, user_form, profile_form)
