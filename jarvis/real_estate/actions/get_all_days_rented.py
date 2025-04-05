import os.path
import subprocess
from django.contrib import messages


class SumAllDaysRented:

    def __init__(self):
        self.all_days = set()
        self.years = {}
        self.success_messages = []

    def reset_all_attributes(self):
        self.all_days = set()
        self.years = {}

    def set_all_days(self, request, queryset):
        for item in queryset:
            item.generate_all_days()
            if item.all_days:
                self.all_days.update(item.all_days)

    def identify_years(self):
        for d in self.all_days:
            year = d.year  # Extract the year from the date
            if year in self.years:
                self.years[year] += 1  # Increment the count for the year
            else:
                self.years[year] = 1  # Initialize the count for the year

    def write_results(self, request):
        self.success_messages.append("total occupied days = {}".format(self.years))
        for message in self.success_messages:
            messages.add_message(request, messages.INFO, message)

    def handle(self, request, queryset):
        self.success_messages = ["Here are the results for the {} selected rents".format(len(queryset))]
        self.set_all_days(request, queryset)
        self.identify_years()
        self.write_results(request)
