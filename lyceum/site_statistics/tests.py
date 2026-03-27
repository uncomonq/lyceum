__all__ = ()
import datetime
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Item
from rating.models import Rating
from users.models import Profile

User = get_user_model()


class StatisticsViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Статистика категория",
            slug="statistics-category",
            weight=5,
        )
        cls.item_1 = Item.objects.create(
            name="Товар 1 статистика",
            text="<p>Это превосходно тестовый товар 1.</p>",
            category=cls.category,
            is_published=True,
        )
        cls.item_2 = Item.objects.create(
            name="Товар 2 статистика",
            text="<p>Это превосходно тестовый товар 2.</p>",
            category=cls.category,
            is_published=True,
        )
        cls.item_3 = Item.objects.create(
            name="Товар 3 статистика",
            text="<p>Это превосходно тестовый товар 3.</p>",
            category=cls.category,
            is_published=True,
        )
        cls.item_4 = Item.objects.create(
            name="Товар 4 статистика",
            text="<p>Это превосходно тестовый товар 4.</p>",
            category=cls.category,
            is_published=True,
        )

        cls.user_1 = User.objects.create_user(
            username="stats_user_1",
            password="strong_password_123",
            is_active=True,
        )
        cls.user_2 = User.objects.create_user(
            username="stats_user_2",
            password="strong_password_123",
            is_active=True,
        )
        cls.user_3 = User.objects.create_user(
            username="stats_user_3",
            password="strong_password_123",
            is_active=True,
        )
        cls.user_4 = User.objects.create_user(
            username="stats_user_4",
            password="strong_password_123",
            is_active=True,
        )

        Profile.objects.get_or_create(user=cls.user_1)
        Profile.objects.get_or_create(user=cls.user_2)
        Profile.objects.get_or_create(user=cls.user_3)
        Profile.objects.get_or_create(user=cls.user_4)

        cls.rating_1 = Rating.objects.create(
            item=cls.item_1,
            user=cls.user_1,
            value=5,
        )
        cls.rating_2 = Rating.objects.create(
            item=cls.item_2,
            user=cls.user_1,
            value=5,
        )
        cls.rating_3 = Rating.objects.create(
            item=cls.item_3,
            user=cls.user_1,
            value=1,
        )
        cls.rating_4 = Rating.objects.create(
            item=cls.item_4,
            user=cls.user_1,
            value=1,
        )
        cls.rating_5 = Rating.objects.create(
            item=cls.item_1,
            user=cls.user_2,
            value=5,
        )
        cls.rating_6 = Rating.objects.create(
            item=cls.item_1,
            user=cls.user_3,
            value=1,
        )
        cls.rating_7 = Rating.objects.create(
            item=cls.item_1,
            user=cls.user_4,
            value=1,
        )

        base = datetime.datetime(
            2026,
            3,
            1,
            tzinfo=datetime.timezone.utc,
        )
        Rating.objects.filter(pk=cls.rating_1.pk).update(
            updated_at=base,
        )
        Rating.objects.filter(pk=cls.rating_2.pk).update(
            updated_at=base + datetime.timedelta(days=1),
        )
        Rating.objects.filter(pk=cls.rating_3.pk).update(
            updated_at=base,
        )
        Rating.objects.filter(pk=cls.rating_4.pk).update(
            updated_at=base + datetime.timedelta(days=2),
        )
        Rating.objects.filter(pk=cls.rating_5.pk).update(
            updated_at=base + datetime.timedelta(days=3),
        )
        Rating.objects.filter(pk=cls.rating_6.pk).update(
            updated_at=base,
        )
        Rating.objects.filter(pk=cls.rating_7.pk).update(
            updated_at=base + datetime.timedelta(days=4),
        )

    def test_users_statistics_selects_last_best_and_worst_items(self):
        response = self.client.get(reverse("statistics:users"))

        self.assertEqual(response.status_code, HTTPStatus.OK)

        user_1_stats = next(
            stat
            for stat in response.context["user_stats"]
            if stat["user"].pk == self.user_1.pk
        )

        self.assertEqual(user_1_stats["best_rating"].item, self.item_2)
        self.assertEqual(user_1_stats["worst_rating"].item, self.item_4)
        self.assertEqual(user_1_stats["rating_count"], 4)
        self.assertEqual(user_1_stats["average_rating"], 3)

    def test_my_items_page_requires_login_and_is_sorted(self):
        response = self.client.get(reverse("statistics:my_items"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        self.client.login(
            username="stats_user_1",
            password="strong_password_123",
        )
        response = self.client.get(reverse("statistics:my_items"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        values = [rating.value for rating in response.context["user_ratings"]]
        self.assertEqual(values, [5, 5, 1, 1])

    def test_items_statistics_shows_average_count_and_last_max_min_users(self):
        response = self.client.get(reverse("statistics:items"))

        self.assertEqual(response.status_code, HTTPStatus.OK)

        item_1_stats = next(
            stat
            for stat in response.context["item_stats"]
            if stat["item"].pk == self.item_1.pk
        )

        self.assertEqual(item_1_stats["rating_count"], 4)
        self.assertEqual(item_1_stats["average_rating"], 3)
        self.assertEqual(item_1_stats["last_max_rating"].user, self.user_2)
        self.assertEqual(item_1_stats["last_min_rating"].user, self.user_4)
