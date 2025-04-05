import tabula
import os
import datetime
from django.contrib import messages


class Results:
    actual_year = str(datetime.datetime.now().year)
    folder_year_results_path = '/home/olivier/Documents/administratif/Aubervilliers/{}/laforet'.format(actual_year)
    extension_filter = '.pdf'

    def get_all_files(self):
        files = os.listdir(self.folder_year_results_path)
        return [file for file in files if file[-4:] == self.extension_filter]

    def get_month_results(self, file):
        dfs = tabula.read_pdf(file, pages='all')
        results = dfs[-1]
        incomes = results['Crédits']
        expenses = results['Débits']
        return {'income': float(incomes[len(incomes) - 2]), 'expenses': float(expenses[len(expenses) - 2]), 'net_income': float(incomes[len(incomes) - 1])}

    def get_year_results_details(self, files):
        results = []
        os.chdir(self.folder_year_results_path)
        for ind, file in enumerate(files):
            print('retrieving data from file {} -- {} on {}'.format(file, ind + 1, len(files)))
            results.append(self.get_month_results(file))
            results[-1]['year'] = file[:4]
            results[-1]['month'] = file[4:6]
            results[-1]['day'] = file[6:8]
        return results

    def get_final_year_results(self, detailed_results):
        income = 0
        expenses = 0
        net_income = 0
        for result in detailed_results:
            income += result.get('income')
            expenses += result.get('expenses')
            net_income += result.get('net_income')
        if round(net_income, 2) == round((income - expenses), 2):
            return {
                detailed_results[0].get('year'): {
                    'income': round(income, 2),
                    'expenses': round(expenses, 2),
                    'net_income': round(net_income, 2),
                    'detailed_results': detailed_results
                }
            }
        else:
            return {}

    def handle(self, request):
        print('-' * 50 + ' GETTING FILES DATA... ' + '-' * 50)
        files = self.get_all_files()
        detailed_results = self.get_year_results_details(files)
        final_results = self.get_final_year_results(detailed_results)
        print(final_results)
        print('-' * 50 + ' DATA PROCESSED ' + '-' * 50)
        messages.add_message(request, messages.INFO, 'data added to the instance')
        return final_results