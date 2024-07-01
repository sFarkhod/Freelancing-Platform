from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import User, Client, Freelancer, StripeCustomer, Payment
from unittest.mock import patch

class PaymentViewSetTest(TestCase):
    def setUp(self):
        self.client_user = User.objects.create(username='clientuser')
        self.freelancer_user = User.objects.create(username='freelanceruser')
        self.client = Client.objects.create(user=self.client_user, balance=1000.00)
        self.freelancer = Freelancer.objects.create(user=self.freelancer_user, balance=0.00)
        self.stripe_client = StripeCustomer.objects.create(user=self.client_user, stripe_customer_id='client_stripe_id')
        self.stripe_freelancer = StripeCustomer.objects.create(user=self.freelancer_user, stripe_customer_id='freelancer_stripe_id')
        self.client = APIClient()

    @patch('stripe.PaymentIntent.create')
    @patch('stripe.Transfer.create')
    def test_create_payment(self, mock_transfer_create, mock_payment_intent_create):
        url = reverse('payment-list')
        data = {
            'client': self.client.id,
            'freelancer': self.freelancer.id,
            'amount': 500.00
        }
        mock_payment_intent_create.return_value = {'id': 'pi_123'}
        mock_transfer_create.return_value = {'id': 'tr_123'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.first()
        self.assertEqual(payment.amount, 500.00)
        self.assertEqual(payment.client, self.client)
        self.assertEqual(payment.freelancer, self.freelancer)
        self.client.refresh_from_db()
        self.freelancer.refresh_from_db()
        self.assertEqual(self.client.balance, 500.00)
        self.assertEqual(self.freelancer.balance, 500.00)
