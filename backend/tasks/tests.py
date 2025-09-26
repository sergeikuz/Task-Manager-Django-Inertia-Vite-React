from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from backend.labels.models import Label
from backend.statuses.models import Status

from .models import Task

User = get_user_model()


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )

        self.another_user = User.objects.create_user(
            username="anotheruser",
            password="testpassword",
            first_name="Another",
            last_name="User",
        )

        self.status = Status.objects.create(name="To Do")
        self.status2 = Status.objects.create(name="In Progress")

        self.label = Label.objects.create(name="Test Label")
        self.label2 = Label.objects.create(name="Second Label")

        self.task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            status=self.status,
            owner=self.user,
            executor=self.user,
        )

        self.task.labels.add(self.label, self.label2)

        self.tasks_url = reverse("tasks:tasks_index")
        self.task_detail_url = reverse(
            "tasks:tasks_detail",
            kwargs={"pk": self.task.id})
        self.task_create_url = reverse("tasks:tasks_create")
        self.task_update_url = reverse(
            "tasks:tasks_update",
            kwargs={"pk": self.task.id})
        self.task_delete_url = reverse(
            "tasks:tasks_delete",
            kwargs={"pk": self.task.id})
        self.login_url = reverse("login")

    def test_task_list_view(self):
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/tasks_index.html")
        self.assertContains(response, "Test Task")
        self.assertContains(response, "To Do")
        self.assertContains(response, "Test User")

        tasks = response.context["tasks"]
        self.assertEqual(len(tasks), 1)
        self.assertIn(self.task, tasks)

    def test_task_detail_view(self):
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/tasks_detail.html")
        self.assertContains(response, "Test Task")
        self.assertContains(response, "Test Description")
        self.assertContains(response, "To Do")
        self.assertContains(response, "Test Label")
        self.assertContains(response, "Second Label")

        task = response.context["task"]
        self.assertEqual(task.id, self.task.id)
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.owner, self.user)
        self.assertEqual(task.executor, self.user)
        self.assertEqual(list(task.labels.all()), [self.label, self.label2])

    def test_task_create_view(self):
        response = self.client.get(self.task_create_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.task_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general_form.html")
        self.assertContains(response, "Создать")

        task_data = {
            "name": "New Task",
            "description": "New Description",
            "status": self.status.id,
            "executor": self.another_user.id,
        }

        response = self.client.post(self.task_create_url, task_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.tasks_url)

        self.assertEqual(Task.objects.count(), 2)
        new_task = Task.objects.get(name="New Task")

        self.assertEqual(new_task.description, "New Description")
        self.assertEqual(new_task.status, self.status)
        self.assertEqual(new_task.executor, self.another_user)
        self.assertEqual(new_task.owner, self.user)

        invalid_task_data = {
            "name": "",
            "description": "Invalid Task",
            "status": self.status.id,
        }

        response = self.client.post(self.task_create_url, invalid_task_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_update_view(self):
        response = self.client.get(self.task_update_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.task_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general_form.html")

        task_data = {
            "name": "Updated Task",
            "description": "Updated Description",
            "status": self.status2.id,
            "executor": self.another_user.id,
            "labels": [self.label.id],
        }

        response = self.client.post(self.task_update_url, task_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.tasks_url)

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")
        self.assertEqual(self.task.description, "Updated Description")
        self.assertEqual(self.task.status, self.status2)
        self.assertEqual(self.task.executor, self.another_user)

        invalid_task_data = {
            "name": "",
            "description": "Invalid Update",
            "status": self.status.id,
            "executor": self.user.id,
        }

        response = self.client.post(self.task_update_url, invalid_task_data)
        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")

    def test_task_delete_view(self):
        response = self.client.get(self.task_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.tasks_url)

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.task_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general_delete_form.html")
        self.assertContains(response, "Да, удалить")

        response = self.client.post(self.task_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_delete_by_not_owner(self):
        self.client.login(username="anotheruser", password="testpassword")
        response = self.client.get(self.task_delete_url)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(self.task_delete_url)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Task.objects.count(), 1)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())

    def test_task_filter(self):
        self.client.login(username="testuser", password="testpassword")

        response = self.client.get(self.tasks_url, {"status": self.status2.id})
        self.assertEqual(response.status_code, 200)

        tasks = response.context["tasks"]
        self.assertNotIn(self.task, tasks)
