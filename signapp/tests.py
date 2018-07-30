from django.test import TestCase
from signapp.models import Account
from signapp.views import signin


# Create your tests here.


class signapp(TestCase):
    def test_student_getall(self):
        response = self.client.get('/app/appstudentinfo/getall/')
        self.assertEqual(response.status_code, 200)

