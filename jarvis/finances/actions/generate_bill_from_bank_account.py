# import datetime
# from dotenv import load_dotenv
# import pdfplumber
# import logging
# from django.contrib import messages
# from real_estate.models import Bill, Asset
# from django.contrib.auth.models import User
#
#
# load_dotenv()
#
# logger = logging.getLogger(__name__)
#
# class DateException(Exception):
#     def __init__(self, message):
#         super().__init__(message)
#
#
# class BillFromBankAccount:
#     ZIP_FILE_NAME = "bank_bills.zip"
#
#     def clean_data(self, raw_data, mapping):
#         """
#         1. identify a line with two consecutive dates and its following line as the same dataset
#         2. gather this dataset in a dict and add it to the clean_data list
#         """
#         first_page_headers_filter = "F.Oper. F.Valor Concepto Importe Saldo"
#         one_page_report_end_filter = "Todoslosimportesdeesteextractoseexpresanen: SALDOANUESTROFAVOR SALDOASUFAVOR"
#         month_filter = " Fechadeemisión: "
#         # step 1:
#         indices_filter = [ind for ind in range(len(raw_data)) if (raw_data[ind] == first_page_headers_filter) or (raw_data[ind] == one_page_report_end_filter) ]
#         raw_data = raw_data[indices_filter[0] + 2:indices_filter[1]]
#         clean_data = []
#         for i in range(len(raw_data)):
#             data = {}
#             if i % 2 != 0:
#                 for key, value in mapping.items():
#                     if key in raw_data[i]:
#                         data.update({"label": value})
#                         columns = raw_data[i-1].split(" ")
#                         if key == "CCPPLASVISTASFUERTURISI-CALLEA" and columns[3] != "-70,00":
#                             data.update({"label": "water"})
#                         data.update(
#                             {
#                                 "date_operation": columns[0],
#                                 "date_value": columns[1],
#                                 "value": columns[3]
#                             }
#                         )
#                         clean_data.append(data)
#                         break
#         return clean_data
#
#     def setup_date(self, original_date):
#         """
#         the format of the bank report is: DD/MM and we need YYYY-MM-DD
#         """
#         now = datetime.datetime.now()
#         logger.info("-" * 200)
#         logger.info("{} | {} | {} | {} |".format(now.month, now.year, original_date[3:], now.month == int(original_date[3:])))
#         if now.month == int(original_date[3:]):
#             year = str(now.year)
#             month = str(now.month)
#         elif now.month == int(original_date[3:]) + 1:
#             logger.info("inside elif")
#             year = str(now.year)
#             month = str(now.month - 1)
#         else:
#             if now.month == 1 and int(original_date[:2]) == 12:
#                 year = str(now.year - 1)
#                 month = str()
#             else:
#                 raise DateException("There is an issue with the month or year of this date: {}".format(original_date))
#         result = year + "-" + month + "-" + original_date[:2]
#         logger.info(result)
#         return result
#
#     def create_bill_instances(self, clean_data, success_messages):
#         """
#         1. enter all the data in the bill instance and save it
#         """
#         for data in clean_data:
#             operation_date = ""
#             try:
#                 operation_date = self.setup_date(data.get("date_operation"))
#             except DateException as e:
#                 logger.info("Error: {}".format(e))
#             instance = Bill()
#             instance.asset = Asset.objects.get(id=2)
#             instance.client_name = User.objects.get(id=1)
#             instance.bill_name = data.get("label")
#             instance.date = operation_date
#             instance.total_price = float(data.get("value").replace(",", ".")[1:])
#             instance.save()
#             success_messages.append("the Bill instance {} have been created.".format(data.get("label")))
#         return success_messages
#
#     def handle(self, request, queryset):
#         """
#             Aim: generate a zip of bill instances to download from monthly bank account report file instance
#             Steps to perform:
#             1. get all the needed data to create a bill:
#                 a. Asset id = 2 (id from Fuerte)
#                 b. client_name id = 1 (Olivier)
#                 c. bill_name
#                 d.date (datefield format)
#                 e. total_price (ex: 123.45)
#
#             2. create a mapping for [bill_name, date, total_price]
#             3. retrieve the file containing to the monthly report pdf
#
#         """
#         logger.info('=' * 200)
#         logger.info(queryset)
#         logger.info('-' * 50 + ' CREATING BILLS INSTANCES ... ' + '-' * 50)
#         # 1. creating mappings for data to retrieve in bank accounts report
#         mapping_label = {"TELEFONICA": "internet",
#                          "TO BE DEFINED": "electricity",
#                          "CCPPLASVISTASFUERTURISI-CALLEA": "copro",
#                          "SECURITASDIRECT": "alarm"}
#         success_messages = []
#         for report_instance in queryset:
#             files = report_instance.FileAccountReport.all()
#             for file in files:
#                 # Access the 'content' field directly from the 'file' instance
#                 # 1. use pdfplumber to get all the raw data from pdf
#                 raw_data = []
#                 with pdfplumber.open(file.content.path) as pdf:
#                     for page in pdf.pages:
#                         # Extract text from the page
#                         text = page.extract_text()
#                         # Split the text into lines
#                         lines = text.split("\n")
#                         # Process lines to extract tabular data
#                         for line in lines:
#                             # logger.info("line = {}".format(line))
#                             # Append the columns to the table_data list
#                             raw_data.append(line)
#
#                 # logger.info(raw_data)
#                 clean_data = self.clean_data(raw_data, mapping_label)
#                 logger.info("-*" * 100)
#                 logger.info("clean_data = {}".format(clean_data))
#                 sucess_messages = self.create_bill_instances(clean_data, success_messages)
#
#
#         [messages.add_message(request, messages.INFO, message) for message in sucess_messages]
#
#
