from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserRegistrationTest(TestCase):

    def test_registration_page_loads(self):
        # Test if the registration page loads successfully
        response = self.client.get(reverse("registration"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_user_registration_valid_data(self):
        # Test if a user can register with valid data
        data = {
            "username": "testuser",
            "password1": "password123",
            "password2": "password123",
            "email": "testuser@example.com",
        }
        response = self.client.post(reverse("registration"), data)
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_user_registration_invalid_passwords(self):
        # Test if registration fails with mismatched passwords
        data = {
            "username": "testuser2",
            "password1": "password123",
            "password2": "wrongpassword",
            "email": "testuser2@example.com",
        }
        response = self.client.post(reverse("registration"), data)
        self.assertFormError(
            response, "form", "password2", "The two password fields didn’t match."
        )

    def test_user_registration_missing_field(self):
        # Test if registration fails with missing fields
        data = {
            "username": "testuser3",
            "password1": "password123",
            "password2": "password123",
        }
        response = self.client.post(reverse("registration"), data)
        self.assertFormError(response, "form", "email", "This field is required.")
