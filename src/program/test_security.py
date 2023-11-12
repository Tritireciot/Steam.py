from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from .views import transfer, BALANCE
from concurrent.futures import ThreadPoolExecutor
from threading import Thread


class SecurityTestCase(TestCase):

    def test_validationerror_when_amount_negative(self):
        amount = -100
        self.assertRaises(ValidationError, transfer, amount)

    def test_http400_when_amount_negative(self):
        amount = -999
        res = self.client.get(reverse('index'), {'amount': amount})

        self.assertEqual(res.status_code, 400)
    
    def tranns(self, amount):
        for _ in range(10 ** 4):
            self.client.get(reverse('index'), {'amount': amount})
    def test_complete_security_tests(self):
        t1 = Thread(target=self.tranns, args=(1,))
        t2 = Thread(target=self.tranns, args=(2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        res = self.client.get(reverse('index'), {'amount': 6})
        self.assertContains(res, f"Transfered {6}")
        self.assertContains(res, f"Your new balance is {10**9 - 10**4 - 2*10**4 - 6}")