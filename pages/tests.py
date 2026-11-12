
from django.test import TestCase
from django.urls import reverse


class PublicPageSmokeTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(
            reverse("pages:home"),
            secure=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_health_check_returns_ok(self):
        response = self.client.get(
            reverse("healthz"),
            secure=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
