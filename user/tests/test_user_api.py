"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse 

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        #Instance a fake client, for make requests in some endpoints.
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        
        #Is one dict with informations for a creation one new user.
        payload = {
            'email':    'test@example.com',
            'password': 'testpass123',
            'name':     'Test Name',
        }

        #Using our client fake to make a post request at endpoint instead.
        res = self.client.post(CREATE_USER_URL, payload)
        
        #Testing if status code have 201 with return. Mens successful 
        # for a new instance in the data base.
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        #Get the user we just created now, by passing email with params.
        user = get_user_model().objects.get(email=payload['email'])
        
        #Test if that user is the same one we just created.
        self.assertTrue(user.check_password(payload['password']))
        
        #Test if have one password in response at post method.
        self.assertNotIn('password', res.data)


    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email':    'test@example.com',
            'password': 'testpass123',
            'name':     'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email':    'test@example.com',
            'password': 'ps2',
            'name':     'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        #Create a dict with the user atributes.
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        #Using the function to create a new user in the system.
        create_user(**user_details)
        #Create a dict with email and password 
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        #Using the client to request a "POST" with url = TOKEN_URL and data = payload.
        res = self.client.post(TOKEN_URL, payload)

        #Testing if have token in data after create a user.
        self.assertIn('token', res.data)
        #Testing if have status code 200 with return for request.
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com', password='goodpass')

        payload = {
            'email': 'test@example.com',
            'password': 'badpass',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    