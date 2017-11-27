from django.test import TestCase, Client
from django.contrib.auth.models import User
import os
from soundboard.models import Sound


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

class SoundUploadTestCase(TestCase):
    def test_upload_sound(self):
        client = Client()
        ryguy = User.objects.create_user('ryguy', 'ryguy@example.com', 'mtxMAPC6ch1EP')
        client.force_login(ryguy, backend=None)

        fixtures_path = os.path.join(os.path.dirname(__file__), 'test_fixtures')

        with open(os.path.join(fixtures_path, 'test_image_file.png'), 'rb') as image_file:
            with open(os.path.join(fixtures_path, 'test_sound_file.wav'), 'rb') as sound_file:
                response = client.post('/sounds/create/', {
                    'name': 'Sound name',
                    'text': 'Sound text',
                    'image_file': image_file,
                    'sound_file': sound_file,
                })

                self.assertEqual(response.status_code, 200)

                json = response.json()

                self.assertIsNotNone(json['id'])
                self.assertEqual(json['name'], 'Sound name')
                self.assertEqual(json['text'], 'Sound text')
                self.assertTrue(json['image_file'].endswith('.png'))
                self.assertTrue(json['sound_file'].endswith('.wav'))

                new_sound = Sound.objects.get(id=json['id'])
                self.assertEqual(new_sound.user, ryguy)
