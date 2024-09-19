from django.test import TestCase
from apps.search.models import SearchLog
from apps.users.models import User

class SearchLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.search_log_data = {
            'user': self.user,
            'query': 'python developer',
            'results_count': 5
        }

    def test_create_search_log(self):
        search_log = SearchLog.objects.create(**self.search_log_data)
        self.assertEqual(search_log.user, self.user)
        self.assertEqual(search_log.query, 'python developer')
        self.assertEqual(search_log.results_count, 5)

    def test_search_log_str_method(self):
        search_log = SearchLog.objects.create(**self.search_log_data)
        expected_str = f"{self.user.email}'s search: python developer"
        self.assertEqual(str(search_log), expected_str)

    def test_search_log_ordering(self):
        SearchLog.objects.create(**self.search_log_data)
        second_search_log = SearchLog.objects.create(
            user=self.user,
            query='java developer',
            results_count=3
        )
        search_logs = SearchLog.objects.all()
        self.assertEqual(search_logs[0], second_search_log)