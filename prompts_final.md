## Índice

1. [Descripción general del producto](#1-descripción-general-del-producto)
2. [Arquitectura del sistema](#2-arquitectura-del-sistema)
3. [Modelo de datos](#3-modelo-de-datos)
4. [Especificación de la API](#4-especificación-de-la-api)
5. [Historias de usuario](#5-historias-de-usuario)
6. [Tickets de trabajo](#6-tickets-de-trabajo)
7. [Pull requests](#7-pull-requests)

---

## 1. Descripción general del producto

**Prompt 1:**
You are a senior product manager and a senior business analyst. I will explain you my business idea and we will refine it untill I am OK. Only then we will start the documentation phase of the project.

**Prompt 2:**
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

**Prompt 3:**
     I like the suggested architecture. We will use it. Now we are clear on that part there is an essential point to take into account. Before starting to play with the MVP. I want to ensure the architecture is working, to do so I want to create an 'Hello World' example with a database info to be sure it can be red, let's say the last month hollidays reservation dates for the flat in FuerteVentura. When this page will be published on internet, then we will start with the MVP work. With this information let's start planning the next steps.


---

## 2. Arquitectura del Sistema

### **2.1. Diagrama de arquitectura:**

**Prompt 1:**
You are a senior software engineer with stong knowledge in backend and infrastructure. Using @personal_database_assistant_prd.md I want you to provide me with a detailed architecture for the MVP phase. Generate a file called MVP_architecture.md in the same folder.

**Prompt 2:**
Update this file so that you provide me with mermaid format for each graph

**Prompt 3:**

### **2.2. Descripción de componentes principales:**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.3. Descripción de alto nivel del proyecto y estructura de ficheros**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.4. Infraestructura y despliegue**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.5. Seguridad**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

### **2.6. Tests**

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

### 3. Modelo de Datos

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

### 4. Especificación de la API

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

### 5. Historias de Usuario

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

### 6. Tickets de Trabajo

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**

---

### 7. Pull Requests

**Prompt 1:**

**Prompt 2:**

**Prompt 3:**