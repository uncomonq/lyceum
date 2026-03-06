__all__ = ()
import mimetypes

from django.conf import settings
import django.http


def download_media(request, file_path):
    media_root = settings.MEDIA_ROOT.resolve()
    media_path = (settings.MEDIA_ROOT / file_path).resolve()

    try:
        media_path.relative_to(media_root)
    except ValueError as error:
        raise django.http.Http404 from error

    if not media_path.is_file():
        raise django.http.Http404

    content_type, _ = mimetypes.guess_type(str(media_path))
    return django.http.FileResponse(
        media_path.open("rb"),
        as_attachment=True,
        filename=media_path.name,
        content_type=content_type or "application/octet-stream",
    )
