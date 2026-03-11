__all__ = ()

from django.apps import apps
import django.db.models


class ItemQuerySet(django.db.models.QuerySet):
    def _for_card(self):
        tag_model = apps.get_model("catalog", "Tag")
        return (
            self.select_related("category")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=tag_model.objects.filter(
                        is_published=True,
                    ).only("name"),
                ),
            )
            .only("name", "text", "category__name")
        )

    def published(self):
        return (
            self.filter(is_published=True, category__is_published=True)
            ._for_card()
            .order_by("category__name", "name")
        )

    def on_main(self):
        return self.published().filter(is_on_main=True).order_by("name")

    def new_items(self, from_datetime):
        return (
            self.filter(created_at__gte=from_datetime)
            ._for_card()
            .order_by("?")[:5]
        )

    def friday_items(self):
        return (
            self.filter(updated_at__week_day=6)
            ._for_card()
            .order_by("-updated_at")[:5]
        )

    def unverified_items(self):
        return self.filter(
            updated_at=django.db.models.F("created_at"),
        )._for_card()


class ItemManager(django.db.models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def on_main(self):
        return self.get_queryset().on_main()

    def new_items(self, from_datetime):
        return self.get_queryset().new_items(from_datetime)

    def friday_items(self):
        return self.get_queryset().friday_items()

    def unverified_items(self):
        return self.get_queryset().unverified_items()
