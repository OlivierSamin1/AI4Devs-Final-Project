from django.urls import path, include
from . import views

urlpatterns = [
    path('bills/download/<str:zip_file_name>/', views.download_bills, name='bills_download'),
    path('renting_bills/download/<str:zip_file_name>/', views.renting_download_bills, name='renting_bills_download'),
    path('bills/download-csv-details/<str:csv_file_name>/', views.download_bills_csv_details, name='bills_download_csv_details'),
]
