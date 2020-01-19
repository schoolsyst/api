import re
import json
import uuid
import random
from urllib.parse import unquote
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from ..models import User
from ..serializers import UserSerializer, UserReadSerializer

client = APIClient()

class UserTests(TestCase):
  def setUp(self):
    User.objects.create_user('user1', 'user1@schoolsyst.com', 'user1spwd')
    User.objects.create_user('user2', 'user2@schoolsyst.com', 'user2spwd')
    User.objects.create_user('user3', 'user3@schoolsyst.com', 'user3spwd')
    User.objects.create_superuser('superuser1', 'superuser1@schoolsyst.com', 'superuser1spwd')
    User.objects.create_superuser('superuser2', 'superuser2@schoolsyst.com', 'superuser2spwd')

  def test_get_a_token(self):
    response = client.post('/api/auth/', {
      'username': 'user1',
      'password': 'user1spwd'
    })
    self.assertIn('token', response.json().keys())
  
  def test_token_is_valid(self):
    response = client.post('/api/auth/', {
      'username': 'user1',
      'password': 'user1spwd'
    })
    token = response.json()['token']
    response = client.get('/api/users/self/', HTTP_AUTHORIZATION=f'Bearer {token}')
    self.assertEqual(response.status_code, 200)
  
class AuthedUserTests(TestCase):
  def setUp(self):
    UserTests.setUp(self)
    token = client.post('/api/auth/', {
      'username': 'user1',
      'password': 'user1spwd'
    }).json()['token']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    self.user = client.get('/api/users/self/').json()
    
  def request_password_reset(self):
    client.post('/api/password-reset/', {
      'email': 'user1@schoolsyst.com'
    }, HTTP_USER_AGENT='')
    
  def test_can_send_reset_password_request(self):
    self.request_password_reset()
    self.assertEqual(len(mail.outbox), 1)
    self.assertEqual(mail.outbox[0].to, ['user1@schoolsyst.com'])
  
  def test_can_change_password_from_email(self):
    self.request_password_reset()
    email = mail.outbox[0]
    # Parsing the email
    token = re.search(r'token=(\w+)', email.body).group(1)
    email = unquote(re.search(r'email=(.+)', email.body).group(1))
    # Requesting the new password
    new_pass = uuid.uuid4()
    response = client.post('/api/password-reset/confirm/', {
      'password': new_pass,
      'token': token
    })
    self.assertTrue(str(response.status_code).startswith('2'), msg=f"Status code is {response.status_code}")
    # Trying to log in
    response = client.post('/api/auth/', {
      'username': 'user1',
      'password': new_pass
    })
    self.assertEqual(response.status_code, 200)
  
class SubjectTests(TestCase):
  def setUp(self):
    AuthedUserTests.setUp(self)
    self.subjects_len = 10
    names = [ uuid.uuid4() for i in range(self.subjects_len) ]
    for name in names:
      client.post('/api/subjects/', {
        'name': name,
        'color': '#000000',
        'weight': random.randint(1, 10)
      })

  def test_can_post_subject(self):
    response = client.post('/api/subjects/', {
      'name': 'philosophie',
      'color': '#f00',
      'weight': 4
    })
    self.assertEqual(response.status_code, 201)

  def test_can_get_subjects(self):
    response = client.get('/api/subjects/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.json()), self.subjects_len)
