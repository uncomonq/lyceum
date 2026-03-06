__all__ = ("CatalogConfig",)
from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
    verbose_name = "Каталог"

    def ready(self):
        from django_cleanup.signals import cleanup_pre_delete
        from sorl.thumbnail import delete

        def cleanup_sorl_cache(**kwargs):
            file = kwargs.get("file")
            if file is not None:
                delete(file)

        cleanup_pre_delete.connect(
            cleanup_sorl_cache,
            dispatch_uid="catalog.sorl.thumbnail.delete",
        )
