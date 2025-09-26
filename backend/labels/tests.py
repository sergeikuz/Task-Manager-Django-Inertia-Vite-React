from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from backend.labels.models import Label
from backend.statuses.models import Status
from backend.tasks.models import Task

User = get_user_model()


class TestLabel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="test",
            last_name="test",
            username="TestUser",
            password="password123",
        )
        self.label = Label.objects.create(name="Test Label")
        self.label2 = Label.objects.create(name="Second Label")

        self.labels_url = reverse_lazy("labels:labels_index")
        self.create_url = reverse_lazy("labels:labels_create")
        self.update_url = reverse_lazy(
            "labels:labels_update",
            kwargs={"pk": self.label.id})
        self.delete_url = reverse_lazy(
            "labels:labels_delete",
            kwargs={"pk": self.label.id})
        self.login_url = reverse_lazy("login")

    def test_label_list(self):
        response = self.client.get(self.labels_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.client.login(username="TestUser", password="password123")
        response = self.client.get(self.labels_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_index.html")
        self.assertContains(response, self.label.name)
        self.assertContains(response, self.label2.name)

        labels = response.context["labels"]
        self.assertEqual(len(labels), 2)
        self.assertIn(self.label, labels)
        self.assertIn(self.label2, labels)

    def test_label_create(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.client.login(username="TestUser", password="password123")

        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general_form.html")

        response = self.client.post(self.create_url, {"name": "New Label"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.labels_url)
        self.assertEqual(Label.objects.count(), 3)
        self.assertTrue(Label.objects.filter(name="New Label").exists())

        response = self.client.post(self.create_url, {"name": "Test Label"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), 3)

        response = self.client.post(self.create_url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), 3)

    def test_label_update_authorized(self):
        self.client.login(username="TestUser", password="password123")

        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general_form.html")

        response = self.client.post(self.update_url, {"name": "Updated Label"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.labels_url)

        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Updated Label")

        response = self.client.post(self.update_url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Updated Label")

    def test_label_update_unauthorized(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        response = self.client.post(self.update_url, {"name": "Updated Label"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Test Label")

    def test_label_delete_authorized(self):
        self.client.login(username="TestUser", password="password123")

        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "general_delete_form.html")

        self.assertTrue(Label.objects.filter(id=self.label.id).exists())

        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.labels_url)

        self.assertEqual(Label.objects.count(), 1)
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_label_delete_unauthorized(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
        self.assertEqual(Label.objects.count(), 2)

    def test_label_protected_delete(self):
        self.client.login(username="TestUser", password="password123")

        status = Status.objects.create(name="In Progress")

        task = Task.objects.create(
            name="Task with Label",
            description="Task description",
            status=status,
            owner=self.user,
            executor=self.user,
        )
        task.labels.add(self.label)

        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.labels_url)

        self.assertEqual(Label.objects.count(), 2)
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
