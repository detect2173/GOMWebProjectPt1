from django.test import TestCase
from django.urls import reverse

class BasicPagesTest(TestCase):
    def test_home(self):
        r = self.client.get(reverse('home'))
        self.assertEqual(r.status_code, 200)

    def test_pricing(self):
        r = self.client.get(reverse('pricing'))
        self.assertEqual(r.status_code, 200)

    def test_book(self):
        r = self.client.get(reverse('book'))
        self.assertEqual(r.status_code, 200)

    def test_lead_magnet_get(self):
        r = self.client.get(reverse('lead_magnet'))
        self.assertEqual(r.status_code, 200)

    def test_lead_magnet_post(self):
        r = self.client.post(reverse('lead_magnet'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'consent': True
        })
        self.assertEqual(r.status_code, 302)  # redirect to thanks
        self.assertIn(reverse('lead_thanks'), r.url)

    def test_terms(self):
        r = self.client.get(reverse('terms'))
        self.assertEqual(r.status_code, 200)

    def test_privacy(self):
        r = self.client.get(reverse('privacy'))
        self.assertEqual(r.status_code, 200)

    def test_start(self):
        r = self.client.get(reverse('start'))
        self.assertEqual(r.status_code, 200)
