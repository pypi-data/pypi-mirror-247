from django.test import TestCase, Client
from django.urls import reverse

from model_bakery import baker


class GASLoginTestCase(TestCase):
    def test_load(self):
        client = Client()
        response = client.get(reverse("gas:login"))
        self.assertEqual(response.status_code, 200)


class IndexTestCase(TestCase):
    def test_load(self):
        admin_user = baker.make(
            "auth.User",
            username="admin",
            is_superuser=True,
        )

        client = Client()
        response = client.get(reverse("gas:index"))
        self.assertEqual(response.status_code, 302)

        client.force_login(admin_user)
        response = client.get(reverse("gas:index"))
        self.assertEqual(response.status_code, 200)


class GASPasswordResetViewTestCase(TestCase):
    def test_load(self):
        client = Client()
        response = client.get(reverse("gas:reset_password"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gas/reset.html")


class GASPasswordResetDoneViewTestCase(TestCase):
    def test_load(self):
        client = Client()
        response = client.get(reverse("gas:password_reset_done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gas/reset_done.html")


class GASPasswordResetConfirmViewTestCase(TestCase):
    def test_load(self):
        client = Client()
        response = client.get(reverse("gas:password_reset_confirm", kwargs={"uidb64": "uidb64", "token": "token"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gas/reset_confirm.html")


class GASPasswordResetCompleteViewTestCase(TestCase):
    def test_load(self):
        client = Client()
        response = client.get(reverse("gas:password_reset_complete"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gas/reset_complete.html")
