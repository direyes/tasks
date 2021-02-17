from django.contrib.auth.models import User
from django.test import TestCase

from django_dynamic_fixture import G
from rest_framework.test import APIClient

from app.models import Task


class ApiTestCase(TestCase):
    """
    Tests for api
    """

    def setUp(self):
        self.client = APIClient()

        username = 'test-user'
        password = '1234'
        self.user = G(
            User,
            username=username,
        )
        self.user.set_password(password)
        self.user.save()

        self.task = G(
            Task,
            owner=self.user,
        )

        self.client.login(username=username, password=password)

    def test_validations_at_create_task(self):
        """
        test to validate errors at create task
        """

        data={}
        response = self.client.post(
            '/api/tasks/',
            data,
            format='json',
        )

        self.assertEquals(response.status_code, 400)
        response_data = response.json()
        self.assertIn('description', response_data)
        self.assertEquals(response_data['description'], ['This field is required.'])

    def test_create_task_ok(self):
        """
        test success task creation
        """

        description = 'test-description'
        data={
            'description': description,
        }
        response = self.client.post(
            '/api/tasks/',
            data,
            format='json',
        )

        self.assertEquals(response.status_code, 201)
        response_data = response.json()

        self.assertIn('id', response_data)
        self.assertEquals(response_data['description'], description)
        self.assertFalse(response_data['complete'])

    def test_task_list(self):
        """
        test success task list
        """

        user_2 = G(
            User,
        )
        G(
            Task,
            owner=user_2,
        )

        response = self.client.get(
            '/api/tasks/',
            format='json',
        )

        self.assertEquals(response.status_code, 200)

        response_data = response.json()
        self.assertIn('results', response_data)
        self.assertEquals(response_data['count'], 1)
        task = response_data['results'][0]
        self.assertEquals(task['id'], self.task.id)
        self.assertEquals(task['description'], self.task.description)
        self.assertEquals(task['complete'], self.task.complete)

    def test_task_list_looking_for_description(self):
        """
        test success task list looking for description
        """

        response = self.client.get(
            '/api/tasks/?description={0}'.format(self.task.description),
            format='json',
        )

        self.assertEquals(response.status_code, 200)

        response_data = response.json()
        self.assertIn('results', response_data)
        self.assertEquals(response_data['count'], 1)
        task = response_data['results'][0]
        self.assertEquals(task['id'], self.task.id)
        self.assertEquals(task['description'], self.task.description)
        self.assertEquals(task['complete'], self.task.complete)

    def test_task_list_looking_for_bad_description(self):
        """
        test success task list looking for bad description
        """

        response = self.client.get(
            '/api/tasks/?search=bad-description',
            format='json',
        )

        self.assertEquals(response.status_code, 200)

        response_data = response.json()
        self.assertIn('results', response_data)
        self.assertEquals(response_data['count'], 0)

    def test_validations_at_update_task(self):
        """
        test to validate errors at update task
        """

        data={}
        response = self.client.put(
            '/api/tasks/{0}/'.format(self.task.pk),
            data,
            format='json',
        )

        self.assertEquals(response.status_code, 400)
        response_data = response.json()
        self.assertIn('description', response_data)
        self.assertEquals(response_data['description'], ['This field is required.'])

    def test_update_task_ok(self):
        """
        test to validate errors at update task
        """

        description = 'test-description'
        data={
            'description': description,
            'complete': True,
        }
        response = self.client.put(
            '/api/tasks/{0}/'.format(self.task.pk),
            data,
            format='json',
        )

        self.assertEquals(response.status_code, 200)
        response_data = response.json()

        self.assertIn('id', response_data)
        self.assertEquals(response_data['description'], description)
        self.assertTrue(response_data['complete'])

    def test_delete_task_ok(self):
        """
        test to validate errors at update task
        """

        response = self.client.delete(
            '/api/tasks/{0}/'.format(self.task.pk),
            format='json',
        )

        self.assertEquals(response.status_code, 204)

    def test_invalid_user_at_delete_task(self):
        """
        test to validate errors at update task
        """

        user_2 = G(
            User,
        )
        task_2 = G(
            Task,
            owner=user_2,
        )

        response = self.client.delete(
            '/api/tasks/{0}/'.format(task_2.pk),
            format='json',
        )

        self.assertEquals(response.status_code, 404)

    def test_request_no_logged_user(self):
        """
        test to validate request from non logged user
        """

        self.client.logout()

        response = self.client.get(
            '/api/tasks/',
            format='json',
        )

        self.assertEquals(response.status_code, 403)
