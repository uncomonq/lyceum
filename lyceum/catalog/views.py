__all__ = ()
from datetime import timedelta

from django.contrib.auth.views import redirect_to_login
from django.db.models import Avg, Count
import django.shortcuts
import django.utils.timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic

import catalog.models
import rating.forms
import rating.models

ITEMS_CONTEXT_KEY = "items"
ITEM_CONTEXT_KEY = "item"
MAIN_IMAGE_CONTEXT_KEY = "main_image"
ITEM_LIST_TEMPLATE = "catalog/item_list.html"
ITEM_DETAIL_TEMPLATE = "catalog/item.html"


class ItemListView(generic.ListView):
    context_object_name = ITEMS_CONTEXT_KEY
    queryset = catalog.models.Item.objects.published()
    template_name = ITEM_LIST_TEMPLATE
    extra_context = {
        "page_title": "Catalog",
    }


class ItemDetailView(generic.DetailView):
    context_object_name = ITEM_CONTEXT_KEY
    pk_url_kwarg = "pk"
    queryset = catalog.models.Item.objects.published()
    template_name = ITEM_DETAIL_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object
        ratings = item.ratings.all()
        aggregate = ratings.aggregate(
            rating_average=Avg("value"),
            rating_count=Count("id"),
        )

        context[MAIN_IMAGE_CONTEXT_KEY] = getattr(item, "main_image", None)
        context["rating_average"] = aggregate["rating_average"]
        context["rating_count"] = aggregate["rating_count"]
        context["user_rating"] = None

        if self.request.user.is_authenticated:
            user_rating = ratings.filter(user=self.request.user).first()
            context["user_rating"] = user_rating
            context["rating_form"] = kwargs.get(
                "rating_form",
            ) or rating.forms.RatingForm(instance=user_rating)

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        self.object = self.get_object()
        user_rating = rating.models.Rating.objects.filter(
            item=self.object,
            user=request.user,
        ).first()

        if "delete" in request.POST:
            if user_rating is not None:
                user_rating.delete()

            return django.shortcuts.redirect(
                "catalog:item_detail",
                pk=self.object.pk,
            )

        if request.POST.get("value") == "":
            if user_rating is not None:
                user_rating.delete()

            return django.shortcuts.redirect(
                "catalog:item_detail",
                pk=self.object.pk,
            )

        rating_form = rating.forms.RatingForm(
            request.POST,
            instance=user_rating,
        )
        if rating_form.is_valid():
            value = rating_form.cleaned_data["value"]
            if value in (None, ""):
                if user_rating is not None:
                    user_rating.delete()
            else:
                rating.models.Rating.objects.update_or_create(
                    item=self.object,
                    user=request.user,
                    defaults={"value": value},
                )

            return django.shortcuts.redirect(
                "catalog:item_detail",
                pk=self.object.pk,
            )

        context = self.get_context_data(rating_form=rating_form)
        return self.render_to_response(context)


class ItemNewView(generic.ListView):
    context_object_name = ITEMS_CONTEXT_KEY
    template_name = ITEM_LIST_TEMPLATE
    extra_context = {
        "page_title": _("New"),
    }

    def get_queryset(self):
        from_datetime = django.utils.timezone.now() - timedelta(days=7)
        return catalog.models.Item.objects.new_items(from_datetime)


class ItemFridayView(generic.ListView):
    context_object_name = ITEMS_CONTEXT_KEY
    template_name = ITEM_LIST_TEMPLATE
    extra_context = {
        "page_title": _("Friday"),
    }

    def get_queryset(self):
        return catalog.models.Item.objects.friday_items()


class ItemUnverifiedView(generic.ListView):
    context_object_name = ITEMS_CONTEXT_KEY
    template_name = ITEM_LIST_TEMPLATE
    extra_context = {
        "page_title": _("Unverified"),
    }

    def get_queryset(self):
        return catalog.models.Item.objects.unverified_items()
