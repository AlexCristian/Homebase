from django.test import TestCase
from django.core.urlresolvers import reverse


class UserSigninTests(TestCase):
    def setUp(self):
        self.client.post(reverse('homebase:register'),
                         {
                         "name": "The Doctor",
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo",
                         "pic_url": "https://upload.wikimedia.org/wikipedia/"
                         "commons/7/70/Matt_Smith_and_Karen_Gillan_at_"
                         "Salford_%28cropped%29.jpg"
                         })

    def test_existent_user_signin(self):
        response = self.client.post(reverse('homebase:signin'),
                                    {
                                    "email": "doctor@tardis.co.uk",
                                    "password": "geronimo"
                                    }
                                    )
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_user_signin(self):
        response = self.client.post(reverse('homebase:signin'),
                                    {
                                    "email": "john@jcena.us",
                                    "password": "it'sjohncena"
                                    }
                                    )
        self.assertEqual(response.status_code, 404)

    def test_incorrect_credential_signin(self):
        response = self.client.post(reverse('homebase:signin'),
                                    {
                                    "email": "doctor@tardis.co.uk",
                                    "password": "hellosweetie"
                                    }
                                    )
        self.assertEqual(response.status_code, 401)


class UserRegisterTests(TestCase):
    def test_invalid_email(self):
        response = self.client.post(reverse('homebase:register'),
                                    {
                                    "name": "The Doctor",
                                    "email": "doctor.tardis.co.uk",
                                    "password": "geronimo",
                                    "pic_url": "https://upload.wikimedia.org/"
                                    })
        self.assertEqual(response.status_code, 400)

    def test_able_to_register(self):
        response = self.client.post(reverse('homebase:register'),
                                    {
                                    "name": "The Doctor",
                                    "email": "doctor@tardis.co.uk",
                                    "password": "geronimo",
                                    "pic_url": "https://upload.wikimedia.org/"
                                    })
        self.assertEqual(response.status_code, 200)

    def test_register_with_sqlinject(self):
        response = self.client.post(reverse('homebase:register'),
                                    {
                                    "name": "<script>alert('test');</script>",
                                    "email": "doctor.tardis.co.uk",
                                    "password": "geronimo",
                                    "pic_url": "https://upload.wikimedia.org/"
                                    })
        self.assertEqual(response.status_code, 400)


class UserdataTests(TestCase):

    def setUp(self):
        self.client.post(reverse('homebase:register'),
                         {
                         "name": "The Doctor",
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo",
                         "pic_url": "https://upload.wikimedia.org/wikipedia/"
                         "commons/7/70/Matt_Smith_and_Karen_Gillan_at_"
                         "Salford_%28cropped%29.jpg"
                         })

    def test_user_session_data_fetch(self):
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )

        response = self.client.get(reverse('homebase:userdata'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_session_data_fetch(self):
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "gernm"
                         }
                         )

        response = self.client.get(reverse('homebase:userdata'))
        self.assertEqual(response.status_code, 404)

    def test_json_matches_db_data(self):
        self.fail('Test not implemented.')


class UserDashboardTests(TestCase):
    def test_json_matches_db_data(self):
        self.fail('Test not implemented.')


class AssignmentAddTests(TestCase):
    def test_create_assignment_with_epoch_date(self):
        self.fail('Test not implemented.')

    def test_create_invalid_assignment(self):
        self.fail('Test not implemented.')

    def test_create_valid_assignment(self):
        self.fail('Test not implemented.')
