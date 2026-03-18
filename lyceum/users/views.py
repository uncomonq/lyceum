from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings
from .forms import SignUpForm
from .models import Profile


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("users:login")
    template_name = "users/signup.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        Profile.objects.create(user=user)
        return super().form_valid(form)
