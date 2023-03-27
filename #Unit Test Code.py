#Unit Test Code
 
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        # Setting test client for the Flask app
        self.client = app.test_client()
        self.client.testing = True
 
    def test_login(self):
        # Defining the login details for test
        data = dict(username='test', password='test')
        response = self.client.post(
            'http://localhost:8050/login',
            content_type='multipart/form-data',
            data=data
        )
        # Checking whether the response is correct or not
        self.assertEqual(response.status_code, 200)
 
    def test_logout(self):
        # Log the user in for testing the logout feature
        credentials = dict(username='test', password='test')
        rv = self.client.post('/login', data=credentials, follow_redirects=True)

        response = self.client.get(
            'http://localhost:8050/logout',
            content_type='multipart/form-data'
        )
        # Checking whether the response is correct or not
        self.assertEqual(response.status_code, 302)
 
    def test_restricted_page(self):
        # Accessing restricted page without being logged in
        response = self.client.get(
            'http://localhost:8050/restricted_page',
            content_type='multipart/form-data'
        )
        # Checking whether the response is correct or not
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()