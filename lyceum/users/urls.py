from django.urls import path, reverse_lazy

import users.forms
import users.views

app_name = "users"

urlpatterns = [
    path(
        "login/",
        users.views.LoginView.as_view(
            template_name="users/login.html",
            authentication_form=users.forms.UserLoginForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        users.views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "password_change/",
        users.views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=reverse_lazy("users:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        users.views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        users.views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        users.views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        users.views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        users.views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path(
        "signup/",
        users.views.SignUpView.as_view(
            template_name="users/signup.html",
        ),
        name="signup",
    ),
    path("activate/<str:username>/", users.views.activate, name="activate"),
    path(
        "reactivate/<str:username>/",
        users.views.reactivate,
        name="reactivate",
    ),
    path(
        "users/",
        users.views.UserListView.as_view(template_name="users/user_list.html"),
        name="user_list",
    ),
    path(
        "users/<int:pk>/",
        users.views.UserDetailView.as_view(
            template_name="users/user_detail.html",
        ),
        name="user_detail",
    ),
    path("profile/", users.views.profile, name="profile"),
]
