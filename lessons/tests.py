from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from lessons.models import Lesson
from users.models import User


# Create your tests here.


class LessonsTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@mail.ru',
            is_superuser=True,
        )
        self.user.set_password('test')
        self.user.save()
        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.lesson = Lesson.objects.create(
            note_id=3,
            title="Geographi",
            description="Object about world",
        )
        self.lesson.save()

    def test_create_lesson(self):
        data = {
            'note_id': self.lesson.note_id,
            'title': self.lesson.title,
            'description': self.lesson.description
        }

        response = self.client.post('/lesson/create', data=data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertTrue(
            Lesson.objects.all().exists()
        )
