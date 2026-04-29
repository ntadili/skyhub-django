# SkyHub – Django Project Guide

## 🚀 Project Overview

SkyHub is a Django-based web application designed to manage:

* Teams
* Departments
* Meetings
* Internal communication (messages)
* Scheduling

Each team member is responsible for building **specific pages**, while sharing the same backend (models + database).

---

## 🧠 How the Project Works (Simple)

Django has 3 main parts:

### 1. Models (Database)

Located in:

```
main/models.py
```

This defines:

* Users (built-in Django)
* Profiles
* Departments
* Teams
* Meetings

👉 Everyone uses the same models. Everyone CAN ADD new models but NOT CHANGE previous models or create duplicates.

Note: a model is basically a table in the ERD like team, department or code_repository ([https://app.diagrams.net/#G1uOL71CrAuLUbbfMsiOpaxTZx_7ns9gDZ#%7B%22pageId%22%3A%22y7M3dXuC5kAcrrcWm3Rq%22%7D](https://app.diagrams.net/#G1uOL71CrAuLUbbfMsiOpaxTZx_7ns9gDZ#%7B%22pageId%22%3A%22y7M3dXuC5kAcrrcWm3Rq%22%7D))

---

### 2. Views (Logic)

Located in:

```
main/views/
```

Each page has its own file:

* `dashboard_views.py`
* `login_views.py`
* `teams_views.py`
* `messages_views.py`
* `organisation_views.py`
* `schedule_views.py`

👉 This is where you:

* fetch data from models
* send data to templates (templates = HTML pages)

---

### 3. Templates (UI)

Located in:

```
main/templates/
```

Each page has its own folder:

```
dashboard/
teams/
messages/
organisation/
schedule/
login/
```

👉 This is where you:

* build HTML
* display data from views

---

### 4. URLs (Routing)

Located in:

```
main/urls/
```

Each page has its own file.

👉 This connects:

```
URL → View → Template
```

---

## 📂 File Structure (Important)

```
main/
│
├── models.py
├── admin.py
│
├── views/
│   ├── dashboard_views.py
│   ├── login_views.py
│   ├── teams_views.py
│   ├── messages_views.py
│   ├── organisation_views.py
│   └── schedule_views.py
|   └── reports_views.py
│
├── urls/
│   ├── dashboard_urls.py
│   ├── login_urls.py
│   ├── teams_urls.py
│   ├── messages_urls.py
│   ├── organisation_urls.py
│   └── schedule_urls.py
│   └── reports_urls.py
│
├── templates/
│   ├── base.html
│   ├── dashboard/
│   ├── teams/
│   ├── messages/
│   ├── organisation/
│   ├── schedule/
│   └── login/
|   └── reports/
```

---

## 👥 Task Assignment

Each person ONLY works on their page.

### Kirtan – Messages

```
main/views/messages_views.py
main/urls/messages_urls.py
main/templates/messages/messages.html
```

### Elvin – Schedule

```
main/views/schedule_views.py
main/urls/schedule_urls.py
main/templates/schedule/schedule.html
```

### Kamil – Teams

```
main/views/teams_views.py
main/urls/teams_urls.py
main/templates/teams/teams.html
```

### Batuhan – Organisation

```
main/views/organisation_views.py
main/urls/organisation_urls.py
main/templates/organisation/organisation.html
```

### Nasser – Login & Dashboard

```
main/views/dashboard_views.py
main/urls/dashboard_urls.py
main/templates/dashboard/index.html

main/views/login_views.py
main/urls/login_urls.py
main/templates/login/login.html
```

### Reports – Not assigned yet

---

## ⚠️ Important Rules

* Do NOT modify  models without agreement
* Do NOT modify other people’s files
* Keep your work isolated to your page

---

## 🧪 Running the Project

```bash
source venv/bin/activate
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## 🛠 Admin Panel

Go to `/admin` to:

* add teams
* add meetings
* test data

---

## 🔁 Git Workflow (VERY IMPORTANT)

### Branches

Each person works on their own branch:

```
kirtan
elvin
kamil
batuhan
```

---

### Save your work (DO THIS ALWAYS)

```bash
git add .
git commit -m "what you did"
git push origin your-name
```

Example:

```bash
git commit -m "Add schedule page UI"
git push origin elvin
```

---

### Rules

* NEVER push to main
* ALWAYS push to your branch
* commit often
* clear messages to keep everyone on track

---

## 🚀 Final Notes

* Keep it simple
* Focus on your page
* Please ask for help if unsure

---

---

## 📊 Reports & Organisation Modules (Batuhan)

The Reports and Organisation modules extend the system by introducing analytical capabilities and improving the visibility of organisational data. These modules were designed to integrate seamlessly into the existing architecture without affecting other components.

---

### 🔹 Organisation Module

The Organisation module provides a structured overview of the system’s internal structure.

#### Features
- Displays total departments, teams, and members
- Presents data using a clear and structured UI layout
- Dynamically retrieves and updates data from the database
- Improves visibility of organisational relationships

#### Implementation
- `main/views/organisation_views.py`
- `main/urls/organisation_urls.py`
- `main/templates/organisation/organisation.html`

---

### 🔹 Reports Module

The Reports module introduces data analytics and export functionality.

#### Features
- Displays key metrics such as:
  - Total teams
  - Teams without managers
- Provides CSV export functionality for external reporting
- Aggregates system data into meaningful insights

#### Implementation
- `main/views/reports_views.py`
- `main/urls/reports_urls.py`
- `main/templates/reports/reports.html`

---

### 🧩 System Design Approach

Both modules were implemented following strong software engineering principles:

#### Separation of Concerns
Business logic is handled in views, while presentation is managed in templates.

#### Modularity
Each module is independent and does not interfere with other components of the system.

#### Reusability
Code is structured in a way that allows reuse of logic and components.

#### Scalability
The system allows new features (e.g. additional reports or analytics) to be added without modifying existing modules.

---

### 📈 Future Improvements

- PDF export for reports
- Data visualisation (charts and dashboards)
- Advanced filtering and sorting options
- Role-based access control
- Real-time data updates

---

### 🧠 Engineering Reflection

The development of these modules demonstrates:

- Practical application of Django in full-stack development
- Strong understanding of MVC (Model-View-Controller) architecture
- Ability to design modular and scalable systems
- Experience with real-world development workflows (Git branching and feature isolation)

---

### 👨‍💻 Contribution (Batuhan)

#### Organisation Module
- Designed and implemented the organisational overview page
- Developed dynamic metrics (departments, teams, members)
- Integrated backend data with frontend templates
- Improved system usability through structured UI design

#### Reports Module
- Designed and developed a complete reporting system
- Implemented CSV export functionality
- Created data aggregation logic for analytics
- Built a fully independent feature without impacting existing modules

#### Engineering Focus
- Applied modular architecture principles
- Ensured clean separation between logic and UI
- Focused on scalability, maintainability, and real-world usability
---

Good luck
