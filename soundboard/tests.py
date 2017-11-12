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

    def test_login_redirects_to_your_boards(self):
        User.objects.create_user('ryguy', 'ryguy@example.com', 'mtxMAPC6ch1EP')
        client = Client()

        response = client.post('/login/', {
            'username': 'ryguy',
            'password': 'mtxMAPC6ch1EP',
        })

        self.assertEqual(response.url, '/your_boards/')

    def test_get_call_to_login_redirects_to_login_or_signup(self):
        client = Client()

        response = client.get('/login/')

        self.assertEqual(response.url, '/login_or_signup/')

    def test_get_call_to_signup_redirects_to_login_or_signup(self):
        client = Client()

        response = client.get('/signup/')

        self.assertEqual(response.url, '/login_or_signup/')
