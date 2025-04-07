"""
Tests for the Health API endpoints.
"""
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from health.models import Product, Symptom, Bill


class HealthAPITestCase(APITestCase):
    """Base test case for health API tests."""
    
    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create a token for authentication
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Create test data
        self.product = Product.objects.create(
            name="Test Product",
            natural=True,
            child_use=False,
            adult_use=True,
            min_age="18"
        )
        
        self.symptom = Symptom.objects.create(
            name="Test Symptom",
            child=False,
            adult=True
        )
        self.symptom.products.add(self.product)
        
        self.bill = Bill.objects.create(
            company_name="Test Healthcare",
            client_name=self.user,
            bill_name="Test Bill",
            total_price=100.0,
            is_paid=False
        )


class ProductAPITests(HealthAPITestCase):
    """Tests for the Product API endpoints."""
    
    def test_list_products(self):
        """Test retrieving a list of products."""
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_product(self):
        """Test retrieving a single product."""
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Product")


class SymptomAPITests(HealthAPITestCase):
    """Tests for the Symptom API endpoints."""
    
    def test_list_symptoms(self):
        """Test retrieving a list of symptoms."""
        url = reverse('symptom-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_symptom(self):
        """Test retrieving a single symptom."""
        url = reverse('symptom-detail', args=[self.symptom.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Symptom")
    
    def test_symptom_products(self):
        """Test retrieving products associated with a symptom."""
        url = reverse('symptom-products', args=[self.symptom.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Product")


class BillAPITests(HealthAPITestCase):
    """Tests for the Bill API endpoints."""
    
    def test_list_bills(self):
        """Test retrieving a list of bills."""
        url = reverse('bill-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_bill(self):
        """Test retrieving a single bill."""
        url = reverse('bill-detail', args=[self.bill.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bill_name'], "Test Bill") 