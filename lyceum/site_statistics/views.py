__all__ = ()

import django.contrib.auth.mixins
from django.db.models import Avg, Count, F, OuterRef, Subquery
import django.views.generic

import catalog.models
import rating.models
import users.models


class UserStatisticsView(django.views.generic.TemplateView):
    template_name = "statistics/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        best_rating_qs = rating.models.Rating.objects.filter(
            user=OuterRef("pk"),
        ).order_by(
            "-value",
            "-updated_at",
            "-id",
        )
        worst_rating_qs = rating.models.Rating.objects.filter(
            user=OuterRef("pk"),
        ).order_by(
            "value",
            "-updated_at",
            "-id",
        )

        users_qs = users.models.User.objects.annotate(
            rating_count=Count("rating", distinct=True),
            average_rating=Avg("rating__value"),
            best_item_name=Subquery(best_rating_qs.values("item__name")[:1]),
            worst_item_name=Subquery(worst_rating_qs.values("item__name")[:1]),
        ).order_by("username")

        context["user_stats"] = users_qs
        return context


class UserRatedItemsView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    context_object_name = "user_ratings"
    template_name = "statistics/my_items.html"

    def get_queryset(self):
        return self.request.user.ratings.select_related("item").order_by(
            "-value",
            "-updated_at",
            "-id",
        )


class ItemStatisticsView(django.views.generic.TemplateView):
    template_name = "statistics/items.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        max_rating_qs = rating.models.Rating.objects.filter(
            item=OuterRef("pk"),
        ).order_by(
            "-value",
            "-updated_at",
            "-id",
        )
        min_rating_qs = rating.models.Rating.objects.filter(
            item=OuterRef("pk"),
        ).order_by(
            "value",
            "-updated_at",
            "-id",
        )

        items_qs = catalog.models.Item.objects.annotate(
            rating_count=Count("rating", distinct=True),
            average_rating=Avg("rating__value"),
            last_max_rating_user=Subquery(
                max_rating_qs.values("user__username")[:1],
            ),
            last_max_rating_value=Subquery(max_rating_qs.values("value")[:1]),
            last_min_rating_user=Subquery(
                min_rating_qs.values("user__username")[:1],
            ),
            last_min_rating_value=Subquery(min_rating_qs.values("value")[:1]),
        ).order_by(
            F("average_rating").desc(nulls_last=True),
            "-rating_count",
            "name",
        )

        context["item_stats"] = items_qs
        return context
