__all__ = ()
from users.models import User


class ProxyUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not isinstance(
            request.user,
            User,
        ):
            request.user = User.objects.get(pk=request.user.pk)

        return self.get_response(request)
