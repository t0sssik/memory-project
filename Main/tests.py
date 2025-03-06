from django.test import TestCase, Client, RequestFactory, SimpleTestCase
from django.utils import timezone
from .models import *
from collections import deque
from datetime import timedelta
from .functions.stats_functions import get_previous_test, check_stats, update_stats
from .functions.test_functions import (get_today_test, get_latest_tests, get_completion_status, get_test_result,
                                       get_last_ten_days)


class StatsFunctionsTests(TestCase):
    def setUp(self):
        User.objects.create(username='user_with_test', email='test', password='test')
        User.objects.create(username='user_without_test', email='test', password='test')
        Stats.objects.create(user=User.objects.get(username='user_with_test'), streak=2, best_streak=3)
        yesterday = timezone.now() - timedelta(days=1)
        Test.objects.create(user=User.objects.get(username='user_with_test'), date=yesterday.date(), is_completed=True)


    def test_get_previous_test(self):
        """Функция получает данные предыдущего теста, и выводит None, если данных нет"""
        user_with_test = User.objects.get(username='user_with_test')
        user_without_test = User.objects.get(username='user_without_test')
        self.assertIsNone(get_previous_test(user_without_test))
        self.assertIsNotNone(get_previous_test(user_with_test))

    def test_update_stats(self):
        """Функция применяется только после выполнения задания и должно увеличивать число на 1 и изменять рекорд, если
         значение стало больше"""
        user_with_test = User.objects.get(username='user_with_test')
        update_stats(user_with_test)
        stats = Stats.objects.get(user=user_with_test)
        self.assertEqual(stats.streak, 3)
        self.assertEqual(stats.best_streak, 3)
        update_stats(user_with_test)
        stats = Stats.objects.get(user=user_with_test)
        self.assertEqual(stats.streak, 4)
        self.assertEqual(stats.best_streak, 4)

    def test_check_stats(self):
        """Функция считает количество выполненных тестов и записывает это значение, а также обнуляет серию, если
        пропущено или не выполнено"""
        user_with_test = User.objects.get(username='user_with_test')
        check_stats(user_with_test)
        stats = Stats.objects.get(user=user_with_test)
        self.assertEqual(stats.completed, 1)
        self.assertEqual(stats.streak, 2)
        prev_test = get_previous_test(user_with_test)
        prev_test.is_completed = False
        prev_test.save()
        check_stats(user_with_test)
        stats = Stats.objects.get(user=user_with_test)
        self.assertEqual(stats.completed, 0)
        self.assertEqual(stats.streak, 0)

class TestFunctionsTests(TestCase):
    def setUp(self):
        User.objects.create(username='user_with_test', email='test', password='test')
        User.objects.create(username='user_without_test', email='test', password='test')
        Test.objects.create(user=User.objects.get(username='user_with_test'), date=timezone.now(), is_completed=True,
                            correct_memory = 3, correct_action=3, correct_attention=3, correct_speech=3,
                            correct_recognition=3)

    def test_get_today_test(self):
        """Функция возвращает False, если нет данных в БД, иначе возвращает запись из БД"""
        user_with_test = User.objects.get(username='user_with_test')
        user_without_test = User.objects.get(username='user_without_test')
        self.assertIsNotNone(get_today_test(user_with_test))
        self.assertEqual(get_today_test(user_without_test), False)

    def test_get_latest_tests(self):
        """Функция возвращает список из 10 или менее последних пройденных пользователем тестов"""
        user_with_test = User.objects.get(username='user_with_test')
        user_without_test = User.objects.get(username='user_without_test')
        self.assertEqual(get_latest_tests(user_with_test).count(), 1)
        self.assertEqual(get_latest_tests(user_without_test).count(), 0)

    def test_get_completion_status(self):
        user_with_test = User.objects.get(username='user_with_test')
        user_without_test = User.objects.get(username='user_without_test')
        self.assertIsNotNone(get_completion_status(user_with_test))
        self.assertEqual(get_completion_status(user_without_test), False)

    def test_get_results(self):
        user_with_test = User.objects.get(username='user_with_test')
        self.assertEqual(get_test_result(user_with_test), (75, 15))

    def test_get_last_ten_days(self):
        user_with_test = User.objects.get(username='user_with_test')
        self.assertEqual(len(get_last_ten_days(user_with_test)), 10)
        self.assertEqual(type(get_last_ten_days(user_with_test)), deque)

class ViewTests(TestCase):

    def setUp(self):
        user = User.objects.create(username='user_test', email='test', password='test')

    def test_homepage(self):
        client_1 = Client()
        client_2 = Client()
        response_1 = client_1.get('/')
        response_2 = client_2.post('/auth/', {'email': 'test', 'password': 'test'})
        response_2 = client_2.get('/')
        self.assertEqual(response_1.status_code, 200)
        self.assertTemplateUsed(response_1, 'home.html')
        self.assertEqual(response_2.status_code, 200)
        self.assertTemplateUsed(response_2, 'main.html')

    def test_auth_page(self):
        response = self.client.get('/auth/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth.html')
