__all__ = ()
import django.contrib.auth.mixins
from django.db.models import Prefetch
import django.views.generic

import catalog.models
import rating.models
import users.models


class UserStatisticsView(django.views.generic.TemplateView):
    template_name = "statistics/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings_qs = rating.models.Rating.objects.select_related(
            "item",
        ).order_by(
            "-updated_at",
            "-id",
        )
        users_qs = users.models.User.objects.all().prefetch_related(
            Prefetch("ratings", queryset=ratings_qs),
        )
        user_stats = []

        for user in users_qs:
            ratings = list(user.ratings.all())
            rating_count = len(ratings)
            average_rating = None
            best_rating = None
            worst_rating = None

            if ratings:
                average_rating = (
                    sum(rating_obj.value for rating_obj in ratings)
                    / rating_count
                )
                max_value = max(rating_obj.value for rating_obj in ratings)
                min_value = min(rating_obj.value for rating_obj in ratings)

                best_rating = next(
                    rating_obj
                    for rating_obj in ratings
                    if rating_obj.value == max_value
                )
                worst_rating = next(
                    rating_obj
                    for rating_obj in ratings
                    if rating_obj.value == min_value
                )

            user_stats.append(
                {
                    "user": user,
                    "best_rating": best_rating,
                    "worst_rating": worst_rating,
                    "rating_count": rating_count,
                    "average_rating": average_rating,
                },
            )

        context["user_stats"] = user_stats
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
        ratings_qs = rating.models.Rating.objects.select_related(
            "user",
        ).order_by(
            "-updated_at",
            "-id",
        )
        items_qs = catalog.models.Item.objects.all().prefetch_related(
            Prefetch("ratings", queryset=ratings_qs),
        )
        item_stats = []

        for item in items_qs:
            ratings = list(item.ratings.all())
            rating_count = len(ratings)
            average_rating = None
            last_max_rating = None
            last_min_rating = None

            if ratings:
                average_rating = sum(
                    rating_obj.value for rating_obj in ratings
                ) / rating_count
                max_value = max(rating_obj.value for rating_obj in ratings)
                min_value = min(rating_obj.value for rating_obj in ratings)
                last_max_rating = next(
                    rating_obj
                    for rating_obj in ratings
                    if rating_obj.value == max_value
                )
                last_min_rating = next(
                    rating_obj
                    for rating_obj in ratings
                    if rating_obj.value == min_value
                )

            item_stats.append(
                {
                    "item": item,
                    "average_rating": average_rating,
                    "rating_count": rating_count,
                    "last_max_rating": last_max_rating,
                    "last_min_rating": last_min_rating,
                },
            )

        item_stats.sort(
            key=lambda stat: (
                stat["average_rating"] is not None,
                stat["average_rating"] or 0,
                stat["rating_count"],
            ),
            reverse=True,
        )

        context["item_stats"] = item_stats
        return context
