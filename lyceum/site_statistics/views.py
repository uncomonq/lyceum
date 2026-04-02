__all__ = ()

import django.contrib.auth.mixins
from django.db.models import Avg, Count, OuterRef, Subquery
import django.views.generic

import catalog.models
import rating.models
import users.models


class UserStatisticsView(django.views.generic.TemplateView):
    template_name = "statistics/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        best_rating_subquery = (
            rating.models.Rating.objects.filter(
                user_id=OuterRef("pk"),
            )
            .order_by("-value", "-updated_at", "-id")
            .values("pk")[:1]
        )
        worst_rating_subquery = (
            rating.models.Rating.objects.filter(
                user_id=OuterRef("pk"),
            )
            .order_by("value", "-updated_at", "-id")
            .values("pk")[:1]
        )

        users_qs = users.models.User.objects.annotate(
            rating_count=Count("rating"),
            average_rating=Avg("rating__value"),
            best_rating_id=Subquery(best_rating_subquery),
            worst_rating_id=Subquery(worst_rating_subquery),
        )
        users_list = list(users_qs)
        rating_ids = {
            rating_id
            for user in users_list
            for rating_id in (user.best_rating_id, user.worst_rating_id)
            if rating_id is not None
        }
        ratings_by_id = {
            rating_obj.pk: rating_obj
            for rating_obj in rating.models.Rating.objects.filter(
                pk__in=rating_ids,
            ).select_related("item")
        }

        context["user_stats"] = [
            {
                "user": user,
                "best_rating": ratings_by_id.get(user.best_rating_id),
                "worst_rating": ratings_by_id.get(user.worst_rating_id),
                "rating_count": user.rating_count,
                "average_rating": user.average_rating,
            }
            for user in users_list
        ]

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
            ("average_rating").desc(nulls_last=True),
            "-rating_count",
            "name",
        )

        context["item_stats"] = items_qs
        return context
