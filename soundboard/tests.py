from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import os
from soundboard.models import Sound, Soundboard, SoundboardAssociation


def create_user(client):
    user = User.objects.create_user('ryguy', 'ryguy@example.com', 'mtxMAPC6ch1EP')
    client.force_login(user, backend=None)
    return user


fixtures_path = os.path.join(os.path.dirname(__file__), 'test_fixtures')


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

        ryguy = create_user(client)

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


class SoundboardCreateTestCase(TestCase):
    def test_create_soundboard(self):
        client = Client()

        ryguy = create_user(client)

        sound_file = ContentFile('a random string')
        sound_a = Sound.objects.create(name='Mario',
                text='oomph',
                image_file=None,
                sound_file=sound_file,
                user=ryguy)
        sound_b = Sound.objects.create(name='Luigi',
                text='oh no',
                image_file=None,
                sound_file=sound_file,
                user=ryguy)

        response = client.post('/soundboard/create/', {
            'soundboardName': 'The Mario Bros',
            'sounds': ','.join([str(sound_a.id), str(sound_b.id)]),
        })

        self.assertEqual(response.status_code, 200)

        json = response.json()

        self.assertIsNotNone(json['id'])

        new_soundboard = Soundboard.objects.get(id=json['id'])
        self.assertEqual(new_soundboard.name, 'The Mario Bros')
        self.assertEqual(new_soundboard.user, ryguy)
        self.assertEqual(len(new_soundboard.sounds.all()), 2)
        self.assertEqual(new_soundboard.sounds.all()[0], sound_a)
        self.assertEqual(new_soundboard.sounds.all()[1], sound_b)
