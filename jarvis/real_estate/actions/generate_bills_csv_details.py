import os.path
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
import csv
from dotenv import load_dotenv
import logging
from django.utils.safestring import mark_safe

load_dotenv()
logger = logging.getLogger(__name__)


class BillsCsvDetailed:
    def __init__(self):
        self.CSV_FILE_NAME = "bills_csv_detailed.csv"
        self.CSV_PATH = os.path.join('static/files', self.CSV_FILE_NAME)
        self.csv_separator = ";"
        self.date_format = '%Y/%m/%d'
        self.headers = ["asset", "bill_name", "bill_comment", "bill_amount", "bill_date"]
        self.rows = []

    def update_bills_attribute(self, queryset):
        # Iam using the custom save method of Bill to update the names and comments automatically before exporting to CSV
        [bill.save() for bill in queryset]

    def handle(self, request, queryset):
        self.update_bills_attribute(queryset)
        logger.info('[BillsCsvDetailed_handle()]:: csv path = {}'.format(self.CSV_PATH))
        # Create the HttpResponse object with the appropriate CSV header.
        # Open the file for writing
        with open(self.CSV_PATH, 'w', newline='') as csvfile:
            # Create a CSV writer using the file
            writer = csv.writer(csvfile, delimiter=self.csv_separator)
            # Write the header row
            writer.writerow(self.headers)
            for bill in queryset:
                bill_date = bill.date.strftime(self.date_format) or ""
                writer.writerow([bill.asset.nickname, bill.bill_name, bill.bill_comment, bill.total_price, bill_date])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.CSV_PATH}"'

        # Create a download link in the message
        download_url = reverse('bills_download_csv_details', args=[self.CSV_FILE_NAME])
        message = mark_safe(f"<a href='http://192.168.1.128:8000{download_url}'>Download the csv of the bills details</a>")
        messages.add_message(request, messages.INFO, message)

        return response