from django.test import TestCase
from .models import Account


class AccountTests(TestCase):
    def setUp(self):
        Account.objects.create(account_id="123", name="moaz tareq", opening_balance=1000, current_balance=1000)
        Account.objects.create(account_id="456", name="ahmed salama", opening_balance=500, current_balance=500)

    def test_transfer_funds(self):
        source = Account.objects.get(account_id="123")
        target = Account.objects.get(account_id="456")

        source.current_balance -= 200
        target.current_balance += 200
        source.save()
        target.save()

        self.assertEqual(source.current_balance, 800)
        self.assertEqual(target.current_balance, 700)