import datetime
from jarvis import settings
import os
import io
import subprocess
import zipfile
from dotenv import load_dotenv
import logging
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

load_dotenv()

logger = logging.getLogger(__name__)


class BillRent:
    ZIP_FILE_NAME = "renting_bills.tar"
    LATEX_FILE_NAME = "bill_for_rent_"
    LATEX_PATH = os.path.join(os.path.abspath(settings.BASE_DIR), os.getenv("UPLOADING_FILES_FOLDER_PATH"), LATEX_FILE_NAME)
    TEMPLATE = r"""
    \documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[top=2cm, bottom=2cm, left=2cm, right=2cm]{geometry}

\begin{document}

\section*{FACTURA}

% Vos informations personnelles
\begin{minipage}{0.5\textwidth}
    Olivier SAMIN \\
    c/ doctor Aquilino Hurle 41, 2B, \\
    33203 Gijon, Asturias \\
    NIE: Y7397087W \\
    Tel: 682882017 \\
    oliviersamin@gmail.com
\end{minipage}
\hfill
% Informations du client
\begin{minipage}{0.4\textwidth}
    \raggedleft
    \textbf{Cliente} \\
    {client_name} \\
    DNI: {client_dni} \\
    {client_address1} \\
    {client_address2} \\
    {client_address3}
\end{minipage}

\bigskip

% Informations de facturation
\section*{Información de Facturación}
\begin{itemize}
    \item Numero de factura: {bill_number}
    \item Fecha: {bill_date}
\end{itemize}

\bigskip

% Tableau des concepts et montants
\section*{Conceptos y Montos}
\begin{tabular}{|p{0.6\textwidth}|p{0.3\textwidth}|}
    \hline
    \textbf{Concepto} & \textbf{Importe (euros)} \\
    Alquiler & \\ 
    Agencia: {platform_name} \\
    Apartemiento: OceanViewRetreat \\
    Localisacion: Corralejo \\
    Fecha de entrada: {entry_date}. \\
    Fecha de salida: {exit_date}} & {brut_price} \\
    \hline
    Importe bruto & {brut_price} \\
    \hline
    Tipo de IGIC & 7\% \\
    \hline
    IGIC & {igic_amount} \\
    \hline
    TOTAL & {total_price} \\
    \hline
\end{tabular}

\bigskip

% Informations de paiement
\section*{Forma de Pago}
Por fecha de reservación 

Vencimiento: {entry_date}

\end{document}
"""

    def setup_bill_number(self, entry_date):
        bill_number = str(entry_date.year) + '/' + str(entry_date.month) + '-' + str(entry_date.day) + '-001'
        return bill_number

    def setup_data(self, resa):
        date_format = "%d/%m/%Y"
        full_name = resa.renting_person_full_name if resa.renting_person_full_name else ""
        direction = resa.renting_person_direction if resa.renting_person_direction else ""
        dni = resa.renting_person_dni if resa.renting_person_dni else ""
        postcode = resa.renting_person_postcode if resa.renting_person_postcode else ""
        city = resa.renting_person_city if resa.renting_person_city else ""
        region = resa.renting_person_region if resa.renting_person_region else ""
        country = resa.renting_person_country if resa.renting_person_country else ""
        bill_date = datetime.datetime.strftime(resa.entry_date, date_format) if resa.entry_date else ""
        bill_number = self.setup_bill_number(resa.entry_date)
        exit_date = datetime.datetime.strftime(resa.end_date, date_format) if resa.end_date else ""
        total_price = str(resa.price) if resa.price else ""
        igic_percentage = 0.07
        brut_price = str(round(float(total_price)/(1+igic_percentage), 2)) if total_price else ""
        igic_amount = str(round(igic_percentage * float(brut_price), 2))
        platform_ame = str(resa.platform) if resa.platform else ""

        data = {
            'client_name': {"value": full_name, "string": "{client_name}"},
            "client_dni": {"value": dni, "string": "{client_dni}"},
            "client_address1": {"value": direction, "string": "{client_address1}"},
            "client_address2": {"value": postcode + ", " + city, "string": "{client_address2}"},
            "client_address3": {"value": region + ", " + country, "string": "{client_address3}"},
            "bill_date": {"value": bill_date, "string": "{bill_date}"},
            "bill_number": {"value": bill_number, "string": "{bill_number}"},
            "entry_date": {"value": bill_date, "string": "{entry_date}"},
            "exit_date": {"value": exit_date, "string": "{exit_date}"},
            "total_price": {"value": total_price, "string": "{total_price}"},
            "brut_price": {"value": brut_price, "string": "{brut_price}"},
            "igic_amount": {"value": igic_amount, "string": "{igic_amount}"},
            "platform_name": {"value": platform_ame, "string": "{platform_name}"}
        }
        return data

    def setup_latex(self, data, latex):
        for key, value in data.items():
            latex = latex.replace(value.get("string"), value.get("value"))
        return latex


    def handle(self, request, queryset):
        """
        1. Create each latex with name including_entry_date and all needed data from Model instance Resa
        2. Generate pdf corresponding and erasinf latex
        3. saving all these pdf in a zip
        """
        logger.info('=' * 200)
        logger.info(queryset)
        logger.info('-' * 50 + ' CREATING PDF... ' + '-' * 50)
        # 1. all data related to resa = income and outomes (cleaning and commissions)
        logger.info('creating latex files ...')
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for index, resa in enumerate(queryset):
                logger.info('creating latex for resa {} ...'.format(resa))
                base_name = self.LATEX_FILE_NAME + str(index)
                latex_file_name = base_name + ".tex"
                latex_path = os.path.join(os.path.abspath(settings.BASE_DIR), os.getenv("UPLOADING_FILES_FOLDER_PATH"), latex_file_name)
                pdf_file_name = base_name + ".pdf"
                pdf_path = os.path.join(os.path.abspath(settings.BASE_DIR), os.getenv("UPLOADING_FILES_FOLDER_PATH"), pdf_file_name)
                data = self.setup_data(resa)
                latex = self.TEMPLATE
                latex = self.setup_latex(data, latex)
                with open(latex_path, "w") as tex_file:
                    tex_file.write(latex)
                logger.info('-' * 200)
                logger.info("latex_path = {}".format(latex_path))
                logger.info("pdf_path = {} | pdf_file_name = {}".format(pdf_path, pdf_file_name))
                try:
                    subprocess.run(["pdflatex", "-interaction=batchmode", latex_path])
                    subprocess.run(["pdflatex", "-interaction=batchmode", latex_path])
                    subprocess.run(["pdflatex", "-interaction=batchmode", latex_path])
                    subprocess.run(["mv", pdf_file_name, pdf_path])
                    zip_file.write(pdf_path, pdf_file_name)
                except subprocess.CalledProcessError:
                    messages.add_message(request, messages.INFO, 'error: The pdf has not been created!')
                os.remove(latex_path)

            # Save the zip file to the desired path
            with open(self.ZIP_FILE_NAME, 'wb') as zip_output:
                zip_output.write(zip_buffer.getvalue())
            subprocess.run(["mv", self.ZIP_FILE_NAME, os.path.join(os.path.abspath(settings.BASE_DIR), os.getenv("UPLOADING_FILES_FOLDER_PATH"))])
            # Prepare the zip file for HTTP response
            response = HttpResponse(zip_buffer.getvalue(), content_type='application/gzip')
            response['Content-Disposition'] = f'attachment; filename="{self.ZIP_FILE_NAME}"'

            # Create a download link in the message
            download_url = reverse('renting_bills_download', args=[self.ZIP_FILE_NAME])
            # message = f'Download the bills zip file here: http://192.168.1.128:8000{download_url}'
            message = mark_safe(f"<a href='http://192.168.1.128:8000{download_url}'>Download the bills zip file</a>")
            messages.add_message(request, messages.INFO, message)

            return response


