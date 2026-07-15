from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from .models import Membership, Organization


class MembershipTests(TestCase):
    def test_user_can_only_join_organization_once(self) -> None:
        user = get_user_model().objects.create_user(username="dani", email="dani@example.com")
        organization = Organization.objects.create(name="Comercio Norte", slug="comercio-norte")
        Membership.objects.create(user=user, organization=organization, role=Membership.Role.OWNER)

        with self.assertRaises(IntegrityError):
            Membership.objects.create(user=user, organization=organization)
