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

Note: a model is basically a table in the ERD like team, department or code_repository (https://app.diagrams.net/#G1uOL71CrAuLUbbfMsiOpaxTZx_7ns9gDZ#%7B%22pageId%22%3A%22y7M3dXuC5kAcrrcWm3Rq%22%7D)

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

Each page has its own file:

* `dashboard_urls.py`
* `teams_urls.py`
* `messages_urls.py`
* etc.

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
│
├── urls/
│   ├── dashboard_urls.py
│   ├── login_urls.py
│   ├── teams_urls.py
│   ├── messages_urls.py
│   ├── organisation_urls.py
│   └── schedule_urls.py
│
├── templates/
│   ├── base.html
│   ├── dashboard/
│   ├── teams/
│   ├── messages/
│   ├── organisation/
│   ├── schedule/
│   └── login/
```

---

## 👥 Task Assignment

Each person ONLY works on their page.

### 🟢 Kirtan – Messages

Work on:

```
main/views/messages_views.py
main/urls/messages_urls.py
main/templates/messages/messages.html
```

---

### 🔵 Elvin – Schedule

Work on:

```
main/views/schedule_views.py
main/urls/schedule_urls.py
main/templates/schedule/schedule.html
```

---

### 🟡 Kamil – Teams

Work on:

```
main/views/teams_views.py
main/urls/teams_urls.py
main/templates/teams/teams.html
```

---

### 🟣 Batuhan – Organisation

Work on:

```
main/views/organisation_views.py
main/urls/organisation_urls.py
main/templates/organisation/organisation.html
```

---

### ⚪ Reports – Not assigned yet

Will follow same structure when implemented.

---

## ⚠️ Important Rules

### ❗ Do NOT modify:

* `models.py` (only if you need to add new models for your page, this is ok and needed)
* other people’s files
* global settings without agreement

---

## 🧪 Running the Project

### Activate virtual environment

```bash
source venv/bin/activate
```

### Run server

```bash
python manage.py runserver
```

### Open in browser

```
http://127.0.0.1:8000/
```

---

## 🛠 Admin Panel (for data)

Go to:

```
/admin
```

Use it to:

* add teams
* add meetings
* test your page data

---

## 🎯 Goal for Each Member

Each person should:

1. Fetch data from models
2. Display it in their page
3. Keep structure clean
4. Not break other pages

---

## 🚀 Final Notes

* Keep things simple
* Focus on your page only

---

## 💬 If stuck

Ask in the group before guessing.

---

Good luck
