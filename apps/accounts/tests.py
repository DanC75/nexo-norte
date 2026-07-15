from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase


class UserTests(TestCase):
    def test_email_must_be_unique(self) -> None:
        user_model = get_user_model()
        user_model.objects.create_user(username="dani", email="dani@example.com")

        with self.assertRaises(IntegrityError):
            user_model.objects.create_user(username="otro", email="dani@example.com")

    def test_string_prefers_full_name(self) -> None:
        user = get_user_model()(
            username="dani", email="dani@example.com", first_name="Dani", last_name="C"
        )
        self.assertEqual(str(user), "Dani C")
