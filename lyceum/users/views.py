__all__ = ()
import datetime

import django.conf
import django.contrib
import django.contrib.auth
import django.contrib.auth.decorators
import django.core.mail
import django.db
import django.shortcuts
import django.urls
import django.utils
import django.views.generic

import users.forms
import users.models
from users.models import Profile

User = django.contrib.auth.get_user_model()

_ACTIVATION_TTL = datetime.timedelta(hours=12)


class SignUpView(django.views.generic.CreateView):
    form_class = users.forms.SignUpForm
    success_url = django.urls.reverse_lazy("users:login")
    template_name = "users/signup.html"

    @django.db.transaction.atomic
    def form_valid(self, form):
        form.instance.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        self.object = form.save()
        Profile.objects.get_or_create(user=self.object)
        self._send_activation_email(self.object.username)
        return django.shortcuts.redirect(self.get_success_url())

    def _send_activation_email(self, username):
        activation_url = self.request.build_absolute_uri(
            django.urls.reverse(
                "users:activate",
                kwargs={"username": username},
            ),
        )
        django.core.mail.send_mail(
            subject="Активация аккаунта",
            message=(
                "Для активации аккаунта перейдите по ссылке:\n"
                f"{activation_url}\n"
                "Ссылка действует 12 часов."
            ),
            from_email=django.conf.settings.DJANGO_MAIL,
            recipient_list=[
                self.object.email or django.conf.settings.DJANGO_MAIL,
            ],
            fail_silently=True,
        )


class UserListView(django.views.generic.ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        user_list = list(users.models.User.objects.active())
        for user in user_list:
            Profile.objects.get_or_create(user=user)

        return user_list


class UserDetailView(django.views.generic.DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user_obj"

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        Profile.objects.get_or_create(user=user)
        return user


@django.contrib.auth.decorators.login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(
        user=request.user,
    )
    if request.method == "POST":
        form = users.forms.ProfileForm(
            request.POST,
            request.FILES,
            instance=profile_obj,
            user=request.user,
        )
        if form.is_valid():
            form.save()
            django.contrib.messages.success(request, "Профиль обновлён")
            return django.shortcuts.redirect("users:profile")
    else:
        form = users.forms.ProfileForm(instance=profile_obj, user=request.user)

    return django.shortcuts.render(
        request,
        "users/profile.html",
        {
            "form": form,
            "profile_obj": profile_obj,
        },
    )


def activate(request, username):
    user = django.shortcuts.get_object_or_404(User, username=username)
    if user.is_active:
        django.contrib.messages.info(request, "Аккаунт уже активирован")
        return django.shortcuts.redirect("users:login")

    if django.utils.timezone.now() - user.date_joined > _ACTIVATION_TTL:
        django.contrib.messages.error(
            request,
            "Срок действия ссылки активации истёк",
        )
        return django.shortcuts.redirect("users:login")

    user.is_active = True
    user.save(update_fields=["is_active"])
    django.contrib.messages.success(request, "Аккаунт успешно активирован")
    return django.shortcuts.redirect("users:login")
