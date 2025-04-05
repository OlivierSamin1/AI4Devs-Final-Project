# import datetime
# import os
# import subprocess
# from django.http import HttpResponse, FileResponse
# from django.contrib import messages
# # from matplotlib import pyplot as plt
#
#
# POSITIF = {'appart1': [123, 12, 23, 2345], 'appart2': [12, 123]}
# NEGATIF = {'appart1': [67, 12, 98], 'appart2': [120, 54]}
#
#
#
# def create_bar_chart(report, xlabel, ylabel, title, file_name, subsection_name):
#     categories = ['Category 1', 'Category 2', 'Category 3']
#     values = [10, 20, 30]
#
#     plt.bar(categories, values)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.title(title)
#     file_path = os.path.join('static/files', file_name)
#     plt.savefig(file_path)  # Save the chart as an image
#     plt.clf()
#     report += "\\subsection{{{}}}\n".format(subsection_name)
#     report += "\\begin{figure}[ht]\n"
#     report += "\\centering\n"
#     report += "\\includegraphics[width=1\\textwidth]{{{}}}\n".format(file_path)
#     report += "\\caption{{{}}}\n".format(subsection_name)
#     report += "\\end{figure}\n"
#     return report
#
#
# def create_pie_chart(report, labels, values, title, file_name, subsection_name):
#     plt.pie(values, labels=labels, autopct='%1.1f%%')
#     plt.title(title)
#     file_path = os.path.join('static/files', file_name)
#     plt.savefig(file_path)  # Save the chart as an image
#     plt.clf()
#     report += "\\subsection{{{}}}\n".format(subsection_name)
#     report += "\\begin{figure}[ht]\n"
#     report += "\\centering\n"
#     report += "\\includegraphics[width=1\\textwidth]{{{}}}\n".format(file_path)
#     report += "\\caption{{{}}}\n".format(subsection_name)
#     report += "\\end{figure}\n"
#     return report
#
# def generate_report(request):
#     title = "General report"
#     subtitle = datetime.date.today().strftime("%Y-%m-%d")
#
#     report = "\\documentclass{article}\n"
#     report += "\\usepackage{graphicx}\n"
#     report += "\\begin{document}\n"
#     report += "\\title{" + title + "}\n"
#     report += "\\author{}\n"
#     report += "\\date{}\n"
#     report += "\\maketitle\n\n"
#     report += "\\section{DATA TO COME}\n\n"
#     report = create_pie_chart(report, ['Label 1', 'Label 2', 'Label 3'], [30, 40, 50], "test title 2", "pieChart.png", "test subsection 2")
#     report = create_bar_chart(report, "test x", "test y", "test title", "barChart.png", "test subsection")
#     report += "\\end{document}"
#
#
#     host_name = request.META.get("HTTP_HOST")
#     tex_file = "static/files/report.tex"  # Update with the correct path inside the container
#     pdf_file = "static/files/report.pdf"  # Update with the correct path inside the container
#
#     with open(tex_file, "w") as f:
#         f.write(report)
#
#     try:
#         subprocess.run(["pdflatex", "-interaction=batchmode", tex_file])
#         subprocess.run(["pdflatex", "-interaction=batchmode", tex_file])
#         subprocess.run(["pdflatex", "-interaction=batchmode", tex_file])
#         subprocess.run(["mv", "report.pdf", pdf_file])
#         messages.add_message(request, messages.INFO, 'pdf successfully created')
#
#         # Send a success message to the client
#     except subprocess.CalledProcessError:
#         messages.add_message(request, messages.INFO, 'error: The pdf has not been created!')
#
#     # Generate a dynamic download link for the PDF file
#     download_url = os.path.join(host_name, pdf_file)
#     messages.add_message(request, messages.INFO, 'Copy and paste in a new tab this url {}'.format(download_url))
#
#     return HttpResponse(status=204)  # Return an empty response
#
#
# # In your Django view, call the generate_report function
# # and return its response
