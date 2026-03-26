__all__ = ()
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Item
from rating.forms import RatingForm
from rating.models import Rating
from users.models import Profile

User = get_user_model()


class RatingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Категория рейтинга",
            slug="rating-category",
            weight=10,
        )
        cls.item = Item.objects.create(
            name="Товар с рейтингом",
            text="<p>Это превосходно хороший товар.</p>",
            category=cls.category,
            is_published=True,
        )

        cls.user = User.objects.create_user(
            username="rating_user",
            password="strong_password_123",
            is_active=True,
        )
        cls.second_user = User.objects.create_user(
            username="rating_user_2",
            password="strong_password_123",
            is_active=True,
        )
        Profile.objects.get_or_create(user=cls.user)
        Profile.objects.get_or_create(user=cls.second_user)

    def test_rating_form_allows_empty_value(self):
        form = RatingForm(data={"value": ""})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["value"], "")

    def test_user_can_create_and_update_single_rating(self):
        self.client.login(
            username="rating_user",
            password="strong_password_123",
        )
        url = reverse("catalog:item_detail", args=[self.item.pk])

        create_response = self.client.post(url, {"value": "4"})

        self.assertEqual(create_response.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            Rating.objects.filter(item=self.item, user=self.user).count(),
            1,
        )
        self.assertEqual(
            Rating.objects.get(item=self.item, user=self.user).value,
            Rating.Value.ADORE,
        )

        update_response = self.client.post(url, {"value": "2"})

        self.assertEqual(update_response.status_code, HTTPStatus.FOUND)
        self.assertEqual(
            Rating.objects.filter(item=self.item, user=self.user).count(),
            1,
        )
        self.assertEqual(
            Rating.objects.get(item=self.item, user=self.user).value,
            Rating.Value.DISLIKE,
        )

    def test_item_detail_shows_rating_stats_and_user_can_delete_rating(self):
        Rating.objects.create(
            item=self.item,
            user=self.user,
            value=Rating.Value.LOVE,
        )
        Rating.objects.create(
            item=self.item,
            user=self.second_user,
            value=Rating.Value.NEUTRAL,
        )

        self.client.login(
            username="rating_user",
            password="strong_password_123",
        )
        url = reverse("catalog:item_detail", args=[self.item.pk])

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["rating_count"], 2)
        self.assertEqual(response.context["rating_average"], 4)
        self.assertEqual(
            response.context["user_rating"].value,
            Rating.Value.LOVE,
        )

        delete_response = self.client.post(url, {"delete": "1"})

        self.assertEqual(delete_response.status_code, HTTPStatus.FOUND)
        self.assertFalse(
            Rating.objects.filter(item=self.item, user=self.user).exists(),
        )
