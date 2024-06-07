from rest_framework import status
from app.tests.test_setup import TestMyModelSetup

class TestMyModelLogAPIs(TestMyModelSetup):
    def test_get_all_my_model(self):
        response = self.client.get('/api/v1/my_model/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)