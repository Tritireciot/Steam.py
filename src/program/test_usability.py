from django.test import TestCase
from django.urls import reverse
from .views import transfer
from django.core.exceptions import ValidationError


class UsabilityTestCase(TestCase):
    def test_http200_when_request_root(self):
        res = self.client.get(reverse('index'))
        self.assertEqual(res.status_code, 200)

    def test_when_valid_amount_httpOk_with_new_balance(self):
        BALANCE = 1000
        amount = 10
        new_balance = BALANCE - amount
        res = self.client.get(reverse('index'), {'amount': amount})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, f"Transfered {amount}")
        self.assertContains(res, f"Your new balance is {new_balance}")

    def test_when_amount_higher_than_balance_httpForbidden(self):
        amount = 1000000
        res = self.client.get(reverse('index'), {'amount': amount})
        self.assertEqual(res.status_code, 400)

    def test_amount_higher_than_balance_validationerror(self):
        amount = 1000000
        self.assertRaises(ValidationError, transfer, amount)
