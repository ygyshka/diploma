from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from lessons.models import Lesson
from users.models import User
from users.serializer import UserRegisterSerializer


# Create your tests here.


class LessonsTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@mail.ru',
            password='test',
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

    def test_create_user(self):
        """Тест  регистрации пользователя """

        user_data = {
            'email': 'test1@mail.ru',
            'password': 'new_test',
            'is_superuser': False
        }
        serializer = UserRegisterSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        self.assertEqual(user.email, user_data['email'])
        self.assertEqual(user.is_staff, user_data['is_superuser'])
        self.assertTrue(user.check_password(user_data['password']))

    def test_create_lesson(self):
        """ Тест создания образовательного модуля """
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
        self.user.is_superuser = False
        self.user.save()
        response = self.client.post('/lesson/create', data=data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_list_lessons(self):
        """ Тест вывода списка образовательных модулей """
        response = self.client.get('/lessons/', format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_retrieve_lesson(self):
        """ Тестирование вывода определенного модуля """
        response = self.client.get(f'/lesson/{self.lesson.id}', format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['title'], self.lesson.title
        )
        self.assertEqual(
            response.data['description'], self.lesson.description
        )

    def test_update_lesson(self):
        """ Тестирование обновления образовательного модуля + тестирование отработки ограничений прав пользователей"""
        data = {
            'title': 'Math',
            'description': 'Science about mathematics'
        }
        response = self.client.put(f'/lesson/update/{self.lesson.id}', data=data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['title'], data['title']
        )
        self.assertEqual(
            response.data['description'], data['description']
        )
        self.user.is_superuser = False
        self.user.save()
        response = self.client.put(f'/lesson/update/{self.lesson.id}', data=data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_delete_lesson(self):
        """ Тестирование удаления образовательного модуля """
        response = self.client.delete(f'/lesson/destroy/{self.lesson.id}', format='json')
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.user.is_superuser = False
        self.user.save()
        response = self.client.delete(f'/lesson/destroy/{self.lesson.id}', format='json')
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )
