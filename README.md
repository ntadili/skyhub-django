# SkyHub

SkyHub is a Django-based internal management web application that brings together the day-to-day workings of an organisation in a single place. It provides a dashboard overview of company health, team and department structure, meeting scheduling, internal messaging, and reporting — all behind user authentication.

The project is built with Django, Django Templates, and Bootstrap 5, and uses SQLite as the default database.

## 🌐 Live Demo

The project is deployed and can be accessed live here:

**[https://skyhub-django-production.up.railway.app/](https://skyhub-django-production.up.railway.app/)**

---

## How to Run

### 1. Activate the virtual environment

```bash
source venv/bin/activate
```

If you don't have a `venv` yet, create one and install the dependencies first:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Apply database migrations

```bash
python manage.py migrate
```

### 3. (Optional) Create an admin user

```bash
python manage.py createsuperuser
```

### 4. Start the development server

```bash
python manage.py runserver
```

Then open your browser at:

```
http://127.0.0.1:8000/
```

The Django admin panel is available at `/admin`.

---

## Contributions

### Nasser Tadili — Project Lead, Sidebar Navigation, Dashboard, Login & Settings

- **Founded the overall structure of the project**: set up the Django project layout, the per-page split of `views/`, `urls/`, and `templates/`, the shared models, the base template / global styling system, and the conventions every teammate followed.
- **Created the main data models** (`Profile`, `Department`, `Team`, `Meeting`) in `main/models.py` and ran the initial migrations that the rest of the team built their features on top of.
- **Managed the Django admin panel** — registered all models in `main/admin.py`, configured list displays / filters, and used it to seed sample data (users, teams, meetings) for the team to test against.
- **Controlled all merges, branches, and conflict resolution** across the team — reviewed pull requests, merged feature branches into `main`, and resolved git conflicts so everyone could keep working in parallel.
- Designed and built the global sidebar navigation (`base.html` / `base.css`) used across every authenticated page.
- Built the **Dashboard** page: hero header, KPI strip (Employees, Clear / At risk / Blocked teams), department headcount chart (Chart.js), upcoming meetings cards, and the searchable / filterable employee directory with a click-to-open employee details modal.
- Implemented the **Login** flow using Django's built-in `LoginView`, with a custom two-pane design and self-registration (`Create account`).
- Built the **Settings** page where logged-in users can view their profile details and change their password.
- Added the logout confirmation modal.

#### Files
- `main/templates/base.html`, `main/static/main/css/base.css`
- `main/templates/dashboard/index.html`, `main/static/main/css/dashboard.css`, `main/views/dashboard_views.py`
- `main/templates/login/login.html`, `main/templates/login/register.html`, `main/views/login_views.py`, `main/urls/login_urls.py`
- `main/templates/settings/settings.html`, `main/views/settings_views.py`, `main/urls/settings_urls.py`

---

### Kirtan — Messages

- Designed and built the internal **Messages** module from the ground up, allowing authenticated users to communicate with each other inside SkyHub.
- Created the `Message` model and added the corresponding migration so messages persist in the database.
- Implemented the **Inbox** view that lists conversations / received messages, with read / unread states.
- Implemented the **Compose** flow: a form to pick a recipient, write a message, and send it.
- Wired the module into the global navigation and ensured it is gated behind authentication via `@login_required`, so only signed-in users can access it.
- Integrated the Messages tab with the rest of the app — the "Message" button on each employee row in the dashboard directory and the "Send message" action in the employee details modal both link straight into this module.

#### Files
- `main/views/messages_views.py`
- `main/urls/messages_urls.py`
- `main/templates/messages/`
- `Message` model in `main/models.py` (+ migration)

---

### Elvin — Meetings (Schedule) & Reports (partial)

- Designed and built the full **Meetings / Schedule** module that powers everything meeting-related in SkyHub.
- Implemented the meeting list view with date / time information, participants, and status, plus the **scheduling UI** that lets users create new meetings.
- Made the schedule page extend the global `base.html` so it shares the sidebar and consistent layout with the rest of the app.
- Surfaced upcoming meetings on the dashboard via the **"Upcoming meetings"** card, which deep-links into this module.
- Contributed partially to the **Reports** module — helped shape the data aggregation and worked alongside Batuhan on the reporting layer.

#### Files
- `main/views/schedule_views.py`
- `main/urls/schedule_urls.py`
- `main/templates/schedule/schedule.html`
- `Meeting` model usage in `main/models.py`
- Partial contributions to `main/views/reports_views.py` and `main/templates/reports/`

---

## Teams Module — Kamil Babouche

### Overview
Implemented the full Teams section of the SkyHub application, allowing users to browse, search, and explore teams across the organisation.

### Features
- **Teams List Page** — Displays all teams in a responsive card grid, each showing the team name, status badge (On Track / At Risk / Blocked), department, team leader, and member count.
- **Search & Filter** — Users can search teams by name and filter by department or status in real time.
- **Team Detail Page** — Clicking a team card opens a dedicated detail page showing full team information and a list of all members with their initials avatar and email address.

### Files Changed
- `main/views/teams_views.py` — Added data querying, filtering logic, and team detail view
- `main/urls/teams_urls.py` — Added URL route for the team detail page
- `main/templates/teams/teams.html` — Built the teams list template with search/filter UI
- `main/templates/teams/team_detail.html` — Created the team detail template with member list

---

## 📊 Reports & Organisation Modules (Batuhan)

The Reports and Organisation modules extend the system by introducing analytical capabilities and improving the visibility of organisational data. These modules were designed to integrate seamlessly into the existing architecture without affecting other components.

---

### 🔹 Organisation Module

The Organisation module provides a structured overview of the system's internal structure.

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
