from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserCRUDTestCase(TestCase):
    def setUp(self):
        # Сначала мы создаем пользователя.
        # Для наполнения базы данными используется метод setUp().
        self.user = User.objects.create_user(
            first_name="test",
            last_name="test",
            username="TestUser",
            password="password123",
        )
        self.second_user = User.objects.create_user(
            first_name="second",
            last_name="second",
            username="SecondUser",
            password="password456",
        )
        # Подготавливаем запросы.
        self.users_url = reverse("users:user_list")
        self.login_url = reverse("login")
        # В самом запросе формируем правильный адрес,
        # подставляя идентификатор созданного пользователя:
        self.update_url = reverse(
            "users:user_update", kwargs={"pk": self.user.id}
        )
        self.delete_url = reverse(
            "users:user_delete", kwargs={"pk": self.user.id}
        )
        self.create_url = reverse("users:user_create")

    def test_user_list(self):
        # Выполняем запрос и проверяем,
        # что он действительно добавил пользователей в базу данных:
        # формирует объект запроса к указанной странице
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("users", response.context)
        users = response.context["users"]
        self.assertTrue(len(users) >= 2)
        self.assertContains(response, "TestUser")
        self.assertContains(response, "SecondUser")
        self.assertTemplateUsed(response, 'users/user_list.html')

    def test_user_create(self):
        # Проверяет создание пользователя
        # Выполняем запрос и проверяем,
        # что он действительно добавил пользователей в базу данных:
        # формирует объект запроса к указанной странице
        # Отправка POST-запроса на изменение
        response = self.client.post(
            self.create_url,
            {
                "first_name": "test2",
                "last_name": "test2",
                "username": "test2user",
                "password1": "password789",
                "password2": "password789",
            },
        )
        # проверяет, что произошел редирект после успешного создания
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)
        self.assertTrue(User.objects.filter(username="test2user").exists())

        response = self.client.get(response.url)
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Пользователь успешно зарегистрирован")

    def test_user_create_invalid(self):
        response = self.client.post(
            self.create_url,
            {
                "first_name": "test3",
                "last_name": "test3",
                "username": "TestUser",
                "password1": "password789",
                "password2": "password789",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "уже существует")

        response = self.client.post(
            self.create_url,
            {
                "first_name": "test3",
                "last_name": "test3",
                "username": "test3user",
                "password1": "password789",
                "password2": "different",
            },
        )
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('password2', form.errors)
        self.assertEqual(
            form.errors['password2'][0],
            "Пароли не совпадают"
        )

    def test_user_update_not_authenticated(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.login_url}")

    def test_user_update_different_user(self):
        self.client.login(username="SecondUser", password="password456")
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            self.update_url,
            {
                "username": "hacked",
                "first_name": "hacked",
                "last_name": "hacked",
                "password1": "hackedpassword",
                "password2": "hackedpassword",
            },
        )
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "TestUser")

    def test_user_update_authenticated(self):
        self.client.login(username="TestUser", password="password123")

        response = self.client.post(
            self.update_url,
            {
                "username": "UpdatedUser",
                "first_name": "Updated",
                "last_name": "Name",
                "password1": "newpassword123",
                "password2": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.users_url)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "UpdatedUser")
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")

        self.client.logout()
        login_success = self.client.login(
            username="UpdatedUser",
            password="newpassword123")
        self.assertTrue(login_success)

        response = self.client.get(self.users_url)
        self.assertContains(response, "UpdatedUser")
        self.assertNotContains(response, "TestUser")

    def test_user_delete_not_authenticated(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.login_url}")

        self.assertTrue(User.objects.filter(id=self.user.id).exists())

    def test_user_delete_different_user(self):
        self.client.login(username="SecondUser", password="password456")
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(User.objects.filter(id=self.user.id).exists())

    def test_user_delete_authenticated(self):
        self.client.login(username="TestUser", password="password123")

        response = self.client.get(self.users_url)
        self.assertContains(response, "TestUser")

        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.users_url)

        self.assertFalse(User.objects.filter(id=self.user.id).exists())

        response = self.client.get(self.users_url)
        self.assertNotContains(response, "TestUser")

    def test_password_length(self):
        response = self.client.post(
            self.create_url,
            {
                "first_name": "test3",
                "last_name": "test3",
                "username": "test3user",
                "password1": "12",
                "password2": "12",
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "слишком короткий")
