from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from tinymce.widgets import TinyMCE

from catalog.admin import ItemAdmin
from catalog.models import Item

__all__ = ("ItemAdminFormWidgetTest",)


class ItemAdminFormWidgetTest(TestCase):
    def test_item_text_uses_tinymce_widget(self):
        admin_obj = ItemAdmin(Item, AdminSite())
        form_class = admin_obj.get_form(request=None)

        self.assertIsInstance(form_class.base_fields["text"].widget, TinyMCE)
