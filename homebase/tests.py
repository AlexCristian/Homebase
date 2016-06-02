from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Course, Assignment, Meeting


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

    def test_user_session_userdata_fetch(self):
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )

        response = self.client.get(reverse('homebase:userdata'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_session_userdata_fetch(self):
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "gernm"
                         }
                         )

        response = self.client.get(reverse('homebase:userdata'))
        self.assertEqual(response.status_code, 404)

    def test_json_matches_db_userdata(self):
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI101",
                         "section": "004"
                         })
        course = Course.objects.get(
            title="CI101"
        )
        self.client.post(reverse('homebase:assignment_new'),
                         {
                         "title": "Have to write essay",
                         "description": "This is a description.",
                         "due_date": "1464870442",
                         "created_at": "1464840442",
                         "type": "PP",
                         "course_id": course.id,
                         "parent_id": "-1"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI102",
                         "section": "009"
                         })
        course2 = Course.objects.get(
            title="CI102"
        )
        self.client.post(reverse('homebase:assignment_new'),
                         {
                         "title": "Have anotherr essay",
                         "description": "This is a description.",
                         "due_date": "1464870442",
                         "created_at": "1464840442",
                         "type": "PP",
                         "course_id": course2.id,
                         "parent_id": "-1"
                         }
                         )

        response = self.client.get(reverse('homebase:userdata'))
        self.assertContains(response, "CI101")
        self.assertContains(response, "CI102")
        self.assertContains(response, "doctor@tardis.co.uk")


class UserDashboardTests(TestCase):
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

    def test_user_session_dashboard_fetch(self):
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )

        response = self.client.get(reverse('homebase:userdata'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_session_dashboard_fetch(self):
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "gernm"
                         }
                         )

        response = self.client.get(reverse('homebase:userdata'))
        self.assertEqual(response.status_code, 404)

    def test_json_matches_db_dashboard(self):
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI101",
                         "section": "004"
                         })
        course = Course.objects.get(
            title="CI101"
        )
        self.client.post(reverse('homebase:assignment_new'),
                         {
                         "title": "Have to write essay",
                         "description": "This is a description.",
                         "due_date": "1464870442",
                         "created_at": "1464840442",
                         "type": "PP",
                         "course_id": course.id,
                         "parent_id": "-1"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI102",
                         "section": "009"
                         })
        course2 = Course.objects.get(
            title="CI102"
        )
        self.client.post(reverse('homebase:assignment_new'),
                         {
                         "title": "Have another essay",
                         "description": "This is a description.",
                         "due_date": "1464870442",
                         "created_at": "1464840442",
                         "type": "PP",
                         "course_id": course2.id,
                         "parent_id": "-1"
                         }
                         )

        response = self.client.get(reverse('homebase:dashboard'))
        self.assertContains(response, "Have to write essay")
        self.assertContains(response, "Have another essay")
        self.assertContains(response, "1464870442")


class AssignmentAddTests(TestCase):
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
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI101",
                         "section": "004"
                         })

    def test_create_assignment_with_epoch_date(self):
        course = Course.objects.get(
            title="CI101"
        )
        response = self.client.post(reverse('homebase:assignment_new'),
                                    {
                                    "title": "Have to write essay",
                                    "description": "This is a description.",
                                    "due_date": "1464870442",
                                    "created_at": "1464840442",
                                    "type": "PP",
                                    "course_id": course.id,
                                    "uemail": "doctor@tardis.co.uk",
                                    "parent_id": "-1"
                                    }
                                    )
        self.assertEqual(response.status_code, 200)

    def test_create_invalid_assignment(self):
        course = Course.objects.get(
            title="CI101"
        )
        response = self.client.post(reverse('homebase:assignment_new'),
                                    {
                                    "title": "Have to write essay",
                                    "description": "This is a description.",
                                    "due_date": "2012-11-01T04:16:13-04:00",
                                    "created_at": "201w1-11-01T04:16:13-04:00",
                                    "type": "PP",
                                    "course_id": course.id,
                                    "uemail": "doctor@tardis.co.uk",
                                    "parent_id": "-1"
                                    }
                                    )
        self.assertEqual(response.status_code, 400)

    def test_create_valid_assignment(self):
        course = Course.objects.get(
            title="CI101"
        )
        response = self.client.post(reverse('homebase:assignment_new'),
                                    {
                                    "title": "Have to write essay",
                                    "description": "This is a description.",
                                    "due_date": "2012-11-01T04:16:13-04:00",
                                    "created_at": "2011-11-01T04:16:13-04:00",
                                    "type": "PP",
                                    "course_id": course.id,
                                    "uemail": "doctor@tardis.co.uk",
                                    "parent_id": "-1"
                                    }
                                    )
        self.assertEqual(response.status_code, 200)


class AssignmentDetailsTests(TestCase):
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
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI101",
                         "section": "004"
                         })
        course = Course.objects.get(
            title="CI101"
        )
        self.client.post(reverse('homebase:assignment_new'),
                         {
                         "title": "Have to write essay",
                         "description": "This is a description.",
                         "due_date": "2012-11-01T04:16:13-04:00",
                         "created_at": "2011-11-01T04:16:13-04:00",
                         "type": "PP",
                         "course_id": course.id,
                         "uemail": "doctor@tardis.co.uk",
                         "parent_id": "-1"
                         }
                         )

    def test_valid_assignment_details(self):
        assignment = Assignment.objects.get(
            title="Have to write essay"
        )
        response = self.client.post(reverse('homebase:assignment_details',
                                            kwargs={'assignment_id':
                                                    assignment.id}
                                            ))
        self.assertEqual(response.status_code, 200)

    def test_invalid_assignment_details(self):
        response = self.client.post(reverse('homebase:assignment_details',
                                            kwargs={'assignment_id': 443}
                                            ))
        self.assertEqual(response.status_code, 404)


class AssignmentDeleteTests(TestCase):
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
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI101",
                         "section": "004"
                         })
        course = Course.objects.get(
            title="CI101"
        )
        self.client.post(reverse('homebase:assignment_new'),
                         {
                         "title": "Have to write essay",
                         "description": "This is a description.",
                         "due_date": "2012-11-01T04:16:13-04:00",
                         "created_at": "2011-11-01T04:16:13-04:00",
                         "type": "PP",
                         "course_id": course.id,
                         "uemail": "doctor@tardis.co.uk",
                         "parent_id": "-1"
                         }
                         )

    def test_valid_assignment_delete(self):
        assignment = Assignment.objects.get(
            title="Have to write essay"
        )
        response = self.client.post(reverse('homebase:assignment_delete',
                                            kwargs={'assignment_id':
                                                    assignment.id}
                                            ))
        self.assertEqual(response.status_code, 200)

    def test_invalid_assignment_delete(self):
        response = self.client.post(reverse('homebase:assignment_delete',
                                            kwargs={'assignment_id': 443}
                                            ))
        self.assertEqual(response.status_code, 404)


class CourseAddTests(TestCase):
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
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )

    def test_add_valid_course(self):
        response = self.client.post(reverse('homebase:course_new'),
                                    {
                                     "title": "CI101",
                                     "section": "004"
                                     })
        self.assertEqual(response.status_code, 200)

    def test_add_invalid_course(self):
        response = self.client.post(reverse('homebase:course_new'),
                                    {
                                     "title": "<script>alert('tst');</script>",
                                     "section": "004"
                                     })
        self.assertEqual(response.status_code, 404)


class CourseDetailsTests(TestCase):
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
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI101",
                         "section": "004"
                         })

    def test_valid_course_details(self):
        course = Course.objects.get(
            title="CI101"
        )
        response = self.client.post(reverse('homebase:course_details',
                                            kwargs={'course_id': course.id}
                                            ))
        self.assertContains(response, "CI101")

    def test_invalid_course_details(self):
        response = self.client.post(reverse('homebase:course_details',
                                            kwargs={'course_id': 3453}
                                            ))
        self.assertEqual(response.status_code, 404)


class MeetingAddTests(TestCase):
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
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI101",
                         "section": "004"
                         })

    def test_add_valid_meeting(self):
        course = Course.objects.get(
            title="CI101"
        )
        response = self.client.post(reverse('homebase:meeting_new'),
                                    {
                                     "course_id": course.id,
                                     "start_time": "14648704420",
                                     "end_time": "1464873442",
                                     "location": "Main",
                                     "recurrence": "W"
                                     })
        self.assertEqual(response.status_code, 200)

    def test_add_invalid_meeting(self):
        course = Course.objects.get(
            title="CI101"
        )
        response = self.client.post(reverse('homebase:meeting_new'),
                                    {
                                     "course_id": course.id,
                                     "start_time": "1464870442",
                                     "end_time": "1464873442",
                                     "location": "Main",
                                     "recurrence": "WEWS"
                                     })
        self.assertEqual(response.status_code, 400)


class MeetingListTests(TestCase):
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
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI101",
                         "section": "004"
                         })
        course = Course.objects.get(
            title="CI101"
        )
        self.client.post(reverse('homebase:meeting_new'),
                         {
                         "course_id": course.id,
                         "start_time": "14648704420",
                         "end_time": "14648704720",
                         "location": "Main",
                         "recurrence": "W"
                         })
        self.client.post(reverse('homebase:meeting_new'),
                         {
                         "course_id": course.id,
                         "start_time": "14648704420",
                         "end_time": "14648704720",
                         "location": "Drexel Plaza",
                         "recurrence": "W"
                         })

    def test_list_valid_meeting(self):
        course = Course.objects.get(
            title="CI101"
        )
        response = self.client.post(reverse('homebase:list_meetings',
                                            kwargs={'course_id': course.id}
                                            ))
        self.assertContains(response, "Main")
        self.assertContains(response, "Drexel Plaza")

    def test_list_invalid_meeting(self):
        response = self.client.post(reverse('homebase:list_meetings',
                                            kwargs={'course_id': 435}
                                            ))
        self.assertEqual(response.status_code, 404)

class MeetingDeleteTests(TestCase):
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
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI101",
                         "section": "004"
                         })
        course = Course.objects.get(
            title="CI101"
        )
        self.client.post(reverse('homebase:meeting_new'),
                         {
                         "course_id": course.id,
                         "start_time": "14648704420",
                         "end_time": "14648704720",
                         "location": "Drexel Plaza",
                         "recurrence": "W"
                         })

    def test_delete_valid_meeting(self):
        meeting = Meeting.objects.get(
            location="Drexel Plaza"
        )
        response = self.client.post(reverse('homebase:meeting_delete',
                                            kwargs={'meeting_id': meeting.id}
                                            ))
        self.assertEqual(response.status_code, 200)

    def test_delete_invalid_meeting(self):
        response = self.client.post(reverse('homebase:meeting_delete',
                                            kwargs={'meeting_id': 435}
                                            ))
        self.assertEqual(response.status_code, 404)


class SubtasksTests(TestCase):
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
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI101",
                         "section": "004"
                         })
        course = Course.objects.get(
            title="CI101"
        )
        self.client.post(reverse('homebase:assignment_new'),
                         {
                     "title": "Have to write essay",
                     "description": "This is a description.",
                     "due_date": "2012-11-01T04:16:13-04:00",
                     "created_at": "2011-11-01T04:16:13-04:00",
                     "type": "PP",
                     "course_id": course.id,
                     "uemail": "doctor@tardis.co.uk",
                     "parent_id": "-1"
                     }
                     )
        task = Assignment.objects.get(
            title="Have to write essay"
        )
        self.client.post(reverse('homebase:assignment_new'),
                         {
                         "title": "Have to write 2 essay",
                         "description": "This is a description.",
                         "due_date": "2012-11-01T04:16:13-04:00",
                         "created_at": "2011-11-01T04:16:13-04:00",
                         "type": "PP",
                         "course_id": course.id,
                         "uemail": "doctor@tardis.co.uk",
                         "parent_id": task.id
                         }
                         )
        self.client.post(reverse('homebase:assignment_new'),
                         {
                         "title": "Another essay",
                         "description": "This is a description.",
                         "due_date": "2012-11-01T04:16:13-04:00",
                         "created_at": "2011-11-01T04:16:13-04:00",
                         "type": "PP",
                         "course_id": course.id,
                         "uemail": "doctor@tardis.co.uk",
                         "parent_id": task.id
                         }
                         )

    def test_valid_assignment_subtasks(self):
        assignment = Assignment.objects.get(
            title="Have to write essay"
        )
        response = self.client.post(reverse('homebase:assignment_subtasks',
                                            kwargs={'assignment_id':
                                                    assignment.id}
                                            ))
        self.assertEqual(response.status_code, 200)

    def test_invalid_assignment_subtasks(self):
        response = self.client.post(reverse('homebase:assignment_subtasks',
                                            kwargs={'assignment_id': 443}
                                            ))
        self.assertEqual(response.status_code, 404)


class AssignmentSetparentTests(TestCase):
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
        self.client.post(reverse('homebase:signin'),
                         {
                         "email": "doctor@tardis.co.uk",
                         "password": "geronimo"
                         }
                         )
        self.client.post(reverse('homebase:course_new'),
                         {
                         "title": "CI101",
                         "section": "004"
                         })
        course = Course.objects.get(
            title="CI101"
        )
        self.client.post(reverse('homebase:assignment_new'),
                         {
                     "title": "Have to write essay",
                     "description": "This is a description.",
                     "due_date": "2012-11-01T04:16:13-04:00",
                     "created_at": "2011-11-01T04:16:13-04:00",
                     "type": "PP",
                     "course_id": course.id,
                     "uemail": "doctor@tardis.co.uk",
                     "parent_id": "-1"
                     }
                     )
        self.client.post(reverse('homebase:assignment_new'),
                         {
                     "title": "Have to write another essay",
                     "description": "This is a description.",
                     "due_date": "2012-11-01T04:16:13-04:00",
                     "created_at": "2011-11-01T04:16:13-04:00",
                     "type": "PP",
                     "course_id": course.id,
                     "uemail": "doctor@tardis.co.uk",
                     "parent_id": "-1"
                     }
                     )

    def test_valid_assignment_setparent(self):
        assignment1 = Assignment.objects.get(
            title="Have to write essay"
        )
        assignment2 = Assignment.objects.get(
            title="Have to write another essay"
        )
        response = self.client.post(reverse('homebase:assignment_setparent',
                                            kwargs={'assignment_id':
                                                    assignment2.id}
                                            ),
                                    {
                                    "parent_id": assignment1.id
                                    })
        self.assertEqual(response.status_code, 200)
        assignment1.refresh_from_db()
        assignment2.refresh_from_db()
        self.assertTrue(assignment2.parent_id.id == assignment1.id)

    def test_invalid_assignment_setparent(self):
        response = self.client.post(reverse('homebase:assignment_setparent',
                                            kwargs={'assignment_id':
                                                    3453}
                                            ),
                                    {
                                    "parent_id": 324
                                    })
        self.assertEqual(response.status_code, 404)
