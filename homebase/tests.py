from django.test import TestCase
from .models import User, Course, Assignment, Meeting
from django.core.urlresolvers import reverse
import hashlib


class UserSigninTests(TestCase):
    def setUp(self):
        self.client.get(reverse('homebase:register'),
                        {
                        "name": "The Doctor",
                        "email": "doctor@tardis.co.uk",
                        "password": "geronimo",
                        "pic_url": "https://upload.wikimedia.org/wikipedia/com"
                        "mons/7/70/Matt_Smith_and_Karen_Gillan_at_Salford_%28c"
                        "ropped%29.jpg"
                        })

    def test_existent_user_signin(self):
        response = self.client.get(reverse('homebase:signin'),
                                   {
                                   "username": "doctor@tardis.co.uk",
                                   "password": hashlib.sha1(
                                        "geronimo"
                                   ).digest()
                                   }
                                   )
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_user_signin(self):
        response = self.client.get(reverse('homebase:signin'),
                                   {
                                   "username": "john@jcena.us",
                                   "password": hashlib.sha1(
                                        "it'sjohncena"
                                   ).digest()
                                   }
                                   )
        self.assertEqual(response.status_code, 404)

    def test_incorrect_credential_signin(self):
        response = self.client.get(reverse('homebase:signin'),
                                   {
                                   "username": "doctor@tardis.co.uk",
                                   "password": hashlib.sha1(
                                        "hellosweetie"
                                   ).digest()
                                   }
                                   )
        self.assertEqual(response.status_code, 401)


class UserRegisterTests(TestCase):
    def test_invalid_username(self):
        self.fail('Test not implemented.')

    def test_able_to_register(self):
        self.fail('Test not implemented.')

    def test_register_with_sqlinject(self):
        self.fail('Test not implemented.')


class UserSessionFetchTests(TestCase):
    def test_user_session_data_fetch(self):
        self.fail('Test not implemented.')


class UserdataTests(TestCase):
    def test_json_matches_db_data(self):
        self.fail('Test not implemented.')


class UserDashboardTests(TestCase):
    def test_json_matches_db_data(self):
        self.fail('Test not implemented.')
