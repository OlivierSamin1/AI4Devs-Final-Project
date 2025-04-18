# Pormpts related to my existing project I need to include for this project:
**Prompt 1 - documents for integration**:
You are a senior product manager and  a senior business analyst. I have my actual personal database which is functional and working. What are all the document I need to create to so that I can integrate this project into a larger one that will use this repo? 


**Prompt 2**:
We will need to create them one by one. You will help me on this work. For each one if you need any information to create the dosument you ask me. You always wait for my validation to continue any action. Some very important points are the following:
- ** The database is on my local NAS on my local network on a Raspberry Pi 3 B+ and is not exposed to internet**
- ** The new softaware will use a new Raspbery Pi 4 on my local network. It will not be connected by any cable to the Raspberry Pi of my database. The new software will be connected to internet**

**Prompt 3**:
- The only authentication method is directly connecting with a computer, opening the address 192.168.1.128/management/ and enter the login and password to acces the database
- So far it does not exist any API endpoints actually, I never used this api module of the project.
- I do not have any documentation as there is no API existing
- No there area not because there is no API
- I want this document to be in a markdown format
you can find the whole database structure o nthe document @database.md 

**Prompt 4**:
That is a good start. The only endpoints I will always use are:
1. Finance/bank account reports
2. Health/bills
3. Real estate/bills
4. Real estate/Hollydays reservation
5. Tax/taxes
update your document

**Prompt 5**:
In any of these endpoints I see an access to the corresponding InLineDocument. This is the key feature as I will need to access and update this documents. I will also need to create instances adding dosmuents to it.

**Prompt 6**:
The idea is that this database will never be exposed to internet. The endpoints will only be used so that the new software that will be created and that will access internet can communicate with it. his new software will need to read but also write data in the database. **I want that the database is never exposed to internet**.  
Update your document as needed

**Prompt 7**:
Perfect, now let's continue to the next needed document. If you need to create diagrams, write them in mermaid format

**Prompt 8**:
My app as well as my postgreSQL are running inside Docker containers, does it change anything? If it does update your work 

**Prompt 9**:
Perfect, let's continue with the next document

**Prompt 10**:
Provide me the data dictionnary fo the models of @document.py @files.py @insurance_company.py and @insurance_contract.py 


**Prompt 11**:
Provide me the data dictionnary fo the models of @bank_account_report.py @bank_account.py @bank_card.py @bank.py and @files.py 


**Prompt 12**:
Provide me the data dictionnary fo the models of @bills.py @files.py @product.py @symptom.py 

**Prompt 13**:
Provide me the data dictionnary fo the models of @asset.py @bills.py @copro_management.py @files.py @hollidays_management.py @mortgage.py @renting_management.py @tenant.py @utilities.py 

**Prompt 14**:
Provide me the data dictionnary fo the models of @files.py @tax_management.py @tax.py 

**Prompt 15**:
Provide me the data dictionnary fo the models of @asset.py @files.py 

**Prompt 16**:
Perfect, let's continue with the next document using @03_data_dictionnary.md to get my all database structure



**Prompt 1 - exploratory phase**:
You are a senior product manager and a senior business analyst. I will explain you my business idea and we will refine it untill I am OK. Only then we will start the documentation phase of the project.

**Prompt 2 - exploratory phase**:
First I have an existing database. You can find all the needed details in @database_documentation . I want to use this database in my new project. This database is on my personal NAS on my local network on a Raspberry Pi 3B and will not be connected to internet. The new software will be on another Raspberry Pi 4 on my local network. It will be the only one connected to internet. These 2 Raspberry pi will not be connected by hardware one with each other. 
The project idea is the following, I want an internet accessible software that can provide the following services:
1. get an AI chatbot with a similar interface to chatgpt that can access my database and answer my questions. e.g: list me all the bills from the month of march 2025 for my  flat in FuerteVentura
2. I want to have several tabs in this software, one of them is a financial  dashboard. I want to chat with the AI and ask him to create figures, charts or tables from the database. e.g: Look at the bank accounts of BBVA and the bank account of Bankinter for the month of March 2025 and create for each of them a pie chart with my income and outcomes. Then create for each of them a chart to represent my outcomes by category (food, leasure...). So I also want to be able to enter personnal categories or add some items to existing categories. I will also need default graphs like the YTD incomes and outcomes for each bank account. So I will need in this tab to have two parts, one with the default graphs and one with the dynamic graphs I ask to the AI.
3. I want another tab to manage my emails from gmail. I have several accounts. I want to ask specific questions about my emails to the AI and it can answer to me. e.g: Look into my emails labeled Aubervilliers and tell me if there are any new message or message from my bank. So I will also need to have listed all the existing labels (by email account) to help my. I will need to be able to use filters for labels and date to filter the emails.
4. Finally I want a tab that will allow me to create instances into my database from an imported document (PDF or image formats). Here is the main idea:
1. there  will be a form with: 
 1.a. a text field for the name of the document
 1.b a dropdown list to select which type of document is imported (health bill, asset bill, CV, tax...)
 1.c. a document downloader that will read if needed the document to get  info depending on the document type
2. there will be a validation part after the form is sent to validate what data will be sent to the database. If the validation is given by the user then the instance is created in the database

**Prompt 3 - exploratory phase**:
Here are the answers to the questions:
1. I need an interactive interface that can handle nice visual effects. I am opened to suggestions for front end but I prefer python/Django if possible for back
2. what are the existing possibilities?
3. I will use an external AI provider, I do not know which one now. The restriction is that the Raspberry Pi 4 cannot handle any load related to the AI 
4. Explain me what are the implication for each one
5. no

**Prompt 4 - exploratory phase**:
I like the suggested architecture. We will use it. Now we are clear on that part there is an essential point to take into account. Before starting to play with the MVP. I want to ensure the architecture is working, to do so I want to create an 'Hello World' example with a database info to be sure it can be red, let's say the last month hollidays reservation dates for the flat in FuerteVentura. When this page will be published on internet, then we will start with the MVP work. With this information let's start planning the next steps.


2025/03/28
---

============== I refactored my old database project and so I have now to recreate the all needed documentation ============

**Prompt 1**:
You are a senior product manager as well as a senior business analyst and a senior software engineer with a strong knowledge in Django, Docker, PostgreSQL, python, linux and Raspberry pi. You are also known to write excellent produc tdocumentation that are always exhaustive, precise and well structured. 
I have the project detailed in the file @database_v2_flattened.md and you also have the@data_dictionnary_from_database.md and@database_ERD.mmd to get the full database details. With these information I want you to build me a README.md. As the file will be large, it would be advised to add specific documentation files inside @project_documentation for each part of the README.md file and then refer to it.

**Prompt 2**:
I want you to add in the file a link to the @database_ERD.mmd file so that the whole strucutre is accessbile for anyone. Then I also want you to generate all the diagras in a mermaid format. Update the @README.md file


2025/03/29
========== I recreate the whole documentation for database integration in the project ================

**Prompt 1**:
You are a senior product manager and  a senior business analyst. 
1. Use @01_raw_first_idea.md and @02_business_idea_refined.md to understna dthe project I want to build. 
2. use all the files in the folder@database_documentation to understand my actual database project that will be connected to the project we are building
3. use @00_integration_documentation_summary.md to generate one by one all the documents  in the folder @database_integration_documentation 


**Prompt2**:
Before generating the other documents, I forgot 2 very important information for my project:
1. I will need to add a data-privacy-vault for my actual database
2. I will need to make a demo so I will need to generate synthetic data that will be accessibleonly for the demo.
Here is what I want you to do:
1. using @01_raw_first_idea.md and @02_business_idea_refined.md you will generate a new file 03_final_project.md in @exploratory_phase to synthetize all these information and adding the new ones
2. Update all the needed filesin @database_integration_documentation 

**Prompt 3**:
you are a senior product manager and a senior business analyst. You will generate the files that are listed in @00_integration_documentation_summary.md and still not yet created in the folder @database_integration_documentation . First read @03_final_project.md and the files inside @database_documentation to understand the new project and the already existing database it will be connected to.

20250330
----

=========== exploratory phase ===================
**Prompt 1**:
Now you will generate a MOSCOW matrix for this project

**Prompt 2**:
You are a senior product manager and a senior business analyst. Using the project documentation @database_integration_documentation and @03_final_project.md you will help me implement the first step of the implementation:  create a 'Hello world' web page with one data coming from my database (we will display for this example the dates of all the last reservations for the flat of FuerteVentura for the month of february 2025). What you have to deliver is:
1. A very complete an detailed document called 01_Hello_world_POC.md where all the steps are detailled. From the hardware steps (setup the Raspberry Pi 4 with its OS, setup the environment, creating the docker containers needed and so on) untill all the software implementation for this step. You will also provide detailed steps to configure a website that can be accesible to anyone (for now)
2. This file will be into a new folder called implementation_steps. 
3. If this file is too large to be created at once, you cancreate sub files for each part and refer to them.

**Prompt 3**:
You have to update your documents for the following info:
1. The Raspberry Pi 3B with  the database is already running and working on my local network, no need for configuration or setup. The application will need to connect to it.
2. The data for February 2025 is already existing in the database. There will be no need to create synthetic data or create any new model in the database. These are already implemented, working and existing data that will be used for this POC

**Prompt 4**:
You have to update the documentation @03_final_project.md to ensure that the following information is taken into account: the whole software inside the Raspberry pi 4 will run inside a docker container (or several if needed, with celery and so on). When updated, you will have to update the documentation in the repo @implementation_steps 

**Prompt 5**:
You dockerized only the backend, I want the whole project dockeriezd, so it means also the front end. Update all the files @03_final_project.md and the repo @implementation_steps 

20250417
---
All the documentation has been generated and I am in the implementation steps (I forgot to copy my previous prompts):

**Prompt 1**:
You are a senior software engineer with strong knowledge of best practices in front end and backend.
check the file @01c_Web_Application.md and follow the instructions in @on-going-step.md and apply them. If you have any doubt just ask questions

**Prompt 2**:
you are a senior software engineer with a strong knowledge in backend, frontend, react and python. You know how to apply all the best practices. You have a strong knowledge in docker and raspberry pi.
My actual project is deployed on a raspberry pi 4. I can ping it on jarvis.localhost. Here is the following behaviour I expect:
1. when no docker container is launch on my raspberry pi 4 I should not have access to my project from my raspberry pi with local IP 192.168.1.129 nor via jarvis.localhost.
2. when I launch my containers I expect to get access to my project trhough jarvis.localhost

The actual behaviour is as follow:
1. when no containers are lauched I have access to my project through 192.1681.129
2. when containers are launched I do not have access to my project through jarvis.localhost

I know that in the corresponding nginx file it is setup as localhost and not jarvis.localhost.

Fix this

**Prompt 3 - using the MCP browser-tools**: 
That's good, now we need to fix the bad request issue. Check my console log to fix it

