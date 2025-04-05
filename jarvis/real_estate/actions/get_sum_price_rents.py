import os.path
import subprocess
from django.contrib import messages


class PriceRent:

    prices = {"total": [], "tax": [], "net": []}
    sum = {"total": 0, "tax": 0, "net": 0}
    success_messages = []


    def set_prices(self, request, queryset):
        self.prices = {"total": [], "tax": [], "net": []}
        for item in queryset:
            self.prices["total"].append(item.price)

    def sum_prices(self):
        self.sum["total"] = round(sum(self.prices["total"]), 2)

    def write_results(self, request):
        self.success_messages.append("renting total = {}".format(self.sum["total"]))
        for message in self.success_messages:
            messages.add_message(request, messages.INFO, message)

    def handle(self, request, queryset):
        self.success_messages = ["Here are the results for the {} rentings selected".format(len(queryset))]
        self.set_prices(request, queryset)
        self.sum_prices()
        self.write_results(request)
