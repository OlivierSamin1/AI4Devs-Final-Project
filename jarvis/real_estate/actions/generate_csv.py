import datetime
from config import settings
import os
import pandas as pd
import csv
from django.contrib import messages
from ..models.hollidays_management import HollydaysReservation
from ..models.bills import Bill
from tax.models.tax import Tax
from dotenv import load_dotenv
import logging
load_dotenv()

logger = logging.getLogger(__name__)


class AssetCsv:
    CSV_FILE_NAME = "raw_results.csv"
    CSV_PATH = os.path.join(os.path.abspath(settings.BASE_DIR), os.getenv("UPLOADING_FILES_FOLDER_PATH"), CSV_FILE_NAME)
    HEADERS = ["appart", "platform", "entry_date", "end_date", "received_money", "cleaning", "platform_commission", "other_commission", "tax", "year", "yearly_price", "bill_name", "bill_date", "bill_price"]
    TAX_FILTER = ["IVI", "Dustbin"]
    def handle(self, request, queryset):
        """
        create 2 csv: 1 of raw_data and one with data_processed
        For each appart, get per year and month:
        1. All incomes
            reservations
        2. All outcomes
            for reservations:
                if R2R -> no outcome
                if booking -> cleaning & platform comission $ Katja
                if AirBnB -> cleaning $ Katja
            IVI & dustbin

        """
        date_format = "%d/%m/%Y"
        logger.info('-' * 50 + ' CREATING CSV... ' + '-' * 50)
        resa = HollydaysReservation.objects.all()
        appart_nicknames = [appart.nickname for appart in queryset]
        resa_validated = []
        resa_validated_csv = []
        # 1. all data related to resa = income and outomes (cleaning and commissions)
        logger.info('Retrieving resa data ...')
        for res in resa:
            # logger.info(res.platform, res.received_money, res.asset.nickname, res.cleaning, res.commission_other, res.commission_platform)
            if res.asset.nickname in appart_nicknames:
                entry_date = res.entry_date
                end_date = res.end_date
                if res.entry_date:
                    entry_date = datetime.datetime.strftime(entry_date, date_format)
                else:
                    entry_date = ""
                if res.end_date:
                    end_date = datetime.datetime.strftime(end_date, date_format)
                else:
                    end_date = ""
                resa_validated.append([res.asset.nickname, res.platform.name, res.entry_date, res.end_date, res.received_money, res.cleaning, res.commission_platform, res.commission_other, "", "", "", "", "", ""])
                resa_validated_csv.append([res.asset.nickname, res.platform.name, entry_date, end_date, res.received_money, res.cleaning, res.commission_platform, res.commission_other, "", "", "", "", "", ""])
        logger.info('Resa data retrieved')
        # 2. Retrieving other outcomes data (IVI, dustbin & Katja comissions)
        taxes = Tax.objects.filter(real_estate_tax_type__in=self.TAX_FILTER)
        taxes_validated = []
        for tax in taxes:
            taxes_validated.append([tax.real_estate_asset.nickname, "", "", "", "", "", "", "", tax.name, tax.year, tax.yearly_price, "", "", ""])
        bills = Bill.objects.filter(is_location_commission_bill=True)
        bills_verified = []
        bills_verified_csv = []
        for bill in bills:
            date = bill.date
            if date:
                date = datetime.datetime.strftime(date, date_format)
            else:
                date = ""
            bills_verified.append([bill.asset.nickname, "", "", "", "", "", "", "", "", "", "", bill.bill_name, bill.date, bill.total_price])
            bills_verified_csv.append([bill.asset.nickname, "", "", "", "", "", "", "", "", "", "", bill.bill_name, date, bill.total_price])

        data = resa_validated + taxes_validated + bills_verified
        data_csv = resa_validated_csv + taxes_validated + bills_verified_csv
        sorted_data = sorted(data, key=lambda x: x[0])
        sorted_data_csv = sorted(data_csv, key=lambda x: (x[0], x[2]))

        # 3. CSV creation
        with open(self.CSV_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.HEADERS)
            writer.writerows(sorted_data_csv)
        logger.info('-' * 50 + ' CSV CREATED ' + '-' * 50)
        messages.add_message(request, messages.INFO, 'csv created {}'.format(self.CSV_PATH))

        # 4. Process raw data
        processed_data = ProcessedDataCsv().handle(self.CSV_PATH)

class ProcessedDataCsv:
    CSV_FILE_NAME = "processed_results.csv"
    CSV_PATH = os.path.join(os.path.abspath(settings.BASE_DIR), os.getenv("UPLOADING_FILES_FOLDER_PATH"), CSV_FILE_NAME)
    HEADERS = ["appart", "year", "month", "raw_income", "income_less_platform", "net_income"]


    def handle(self, raw_data_csv_path):
        """
        1. Use the raw_data coming from AssetCsv instance to get raw data
        2. process the data to get the following final data:
            a. income / month / appart
            b. outcome / month / appart
            c. net result / month / appart
        3. appart, year, month, raw_income, income_less_platform, net_income
        """
        date_format = "%d/%m/%Y"
        # Read the CSV file into a DataFrame
        df = pd.read_csv(raw_data_csv_path)

        # Convert 'entry_date' and 'end_date' columns to datetime objects
        df['entry_date'] = pd.to_datetime(df['entry_date'], format=date_format)
        df['end_date'] = pd.to_datetime(df['end_date'], format=date_format)
        df['bill_date'] = pd.to_datetime(df['bill_date'], format=date_format)

        # Extract year and month from 'end_date'
        df['year'] = df['end_date'].dt.year
        df['month'] = df['end_date'].dt.month
        df['year_tax'] = df['year']

        # Group by 'appart', 'year', and 'month', and calculate the sum of 'received_money'
        raw_income = df.groupby(['appart', 'year', 'month'])['received_money'].sum().reset_index()
        # Group by 'appart' and 'year', and calculate the sum of 'yearly_price'

        # Merge raw_income and fixed_expenses on 'appart' and 'year'
        result = pd.merge(raw_income, fixed_expenses, on=['appart', 'year'], how='left')

        # Calculate the total expenses for each apartment for the year
        result['total_expenses'] = result['yearly_price']

        # Calculate the monthly expense for each apartment
        result['monthly_expense'] = result['total_expenses'] / 12

        # Subtract monthly expenses from the received income for each month
        result['net_income'] = result['received_money'] - result['monthly_expense']

        # Sort the result by 'appart', 'year', and 'month'
        result = result.sort_values(by=['appart', 'year', 'month'])

        logger.info(result)