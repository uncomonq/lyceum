__all__ = ()

import django.conf
import django.contrib
import django.contrib.auth
import django.contrib.auth.decorators
import django.core.mail
import django.shortcuts
import django.urls

import users.forms
import users.models


def signup(request):
    form = users.forms.UserCreationForm(request.POST or None)
    context = {"form": form}

    if request.method == "POST" and form.is_valid():
        user = form.save()
        user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        user = form.save()
        profile = users.models.Profile.objects.create(user=user)
        profile.save()

        activate_url = django.urls.reverse(
            "users:activate",
            kwards={"pk": user.id},
        )
        django.core.mail.send_mail(
            f"Здравствуй {user.username}",
            "Перейди по ссылке для активации аккаунта " f"{activate_url}",
            django.conf.settings.FEEDBACK_SENDER,
            [user.email],
            fail_silently=False,
        )

        return django.shortcuts.redirect(django.urls.reverse("homepage:"))

    return django.shortcuts.render(request, "users/signup.html", context)


def activate(request, pk):
    user = users.models.User.objects.get(pk=pk)
    user.is_active = True
    user.save()
    return django.shortcuts.redirect(django.urls.reverse("homepage:"))


def reactivate(request, pk):
    user = users.models.User.objects.get(pk=pk)
    user.is_active = True
    user.save()


def user_list(request):
    context = {"users": users.models.User.objects.active()}

    return django.shortcuts.render(request, "users/user_list.html", context)


def user_detail(request, pk):
    search_user = django.shortcuts.get_object_or_404(
        users.models.User.objects.active(),
        pk=pk,
    )
    context = {"user": search_user}

    return django.shortcuts.render(request, "users/user_detail.html", context)


@django.contrib.auth.decorators.login_required
def profile(request):
    user_form = users.forms.UserChangeForm(
        request.POST or None,
        instance=request.user,
    )
    profile_form = users.forms.UpdateProfileForm(
        request.POST or None,
        instance=request.user.profile,
    )
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    if (
        request.method == "POST"
        and user_form.is_valid()
        and profile_form.is_valid()
    ):
        user_form.save()
        profile_form.save()
        django.contrib.messages.success(request, "Сохранено")
        return django.shortcuts.redirect(django.urls.redirect("users:profile"))

    return django.shortcuts.render(request, "users/profile.html", context)
