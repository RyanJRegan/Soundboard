from django.test import TestCase, Client
from django.contrib.auth.models import User

class AuthenticationTestCase(TestCase):
    def test_signup_creates_user(self):
        client = Client()
        client.post('/signup/', {
            'username': 'ryguy',
            'email': 'ryguy@example.com',
            'password1': 'mtxMAPC6ch1EP',
            'password2': 'mtxMAPC6ch1EP',
        })

        new_user = User.objects.get(username='ryguy')

        self.assertEqual(new_user.email, 'ryguy@example.com')

    def test_signup_redirects_to_your_boards(self):
        client = Client()
        response = client.post('/signup/', {
            'username': 'ryguy',
            'email': 'ryguy@example.com',
            'password1': 'mtxMAPC6ch1EP',
            'password2': 'mtxMAPC6ch1EP',
        })

        self.assertEqual(response.url, '/your_boards/')
