# Online Learning System

A Django-based web application for managing online learning content with full role based authentication and permission control. It supports three user roles: Employee, Instructor, Student; Each role has different login access, views, and permissions, ensuring that users only see and manage data relevant to their role.

## 🚀 Features

### 👤 Employee (Admin)

- Sees admin dashboard

- Full access to all models (CRUD)

- Can create and manage other employees, instructors, and students

### 👩‍🏫 Instructor

- Sees instructor dashboard with own courses, and enrolled students

- Can perform CRUD operations on category, tag, course, and lesson

- Can only see and manage their own courses

### 👩‍🎓 Student

- Sees student dashboard with enrolled courses

- Can view and enroll in all courses

- Can rate and review courses they are enrolled in

## 📌 Technologies

- Django (Python)

- SQLite3

- HTML / CSS

- Bootstrap

## ⚙️ Development Tools

- Visual Studio Code

- Git

- GitHub

## 🛠️ How To Get Started

1. Clone the repository

```
  https://github.com/Meimei07/django-online-learning-system.git
```

2. Download Python (if you haven't)

3. Install pipenv (globally)

```
  pip install pipenv
```

4. Navigate to project folder and install dependencies (Django & Pillow) using pipenv

```
  pipenv install
```

## 📖 Usage

1. Navigate to project folder and activate the environment

```
  pipenv shell
```

2. Run the server

```
  python manage.py runserver
```

3. Open your browser and go to:

```
  http://127.0.0.1:8000/
```

## 🔍 Exploring the Website

When you open the application, you'll be directed to the login page. You can login using one of the sample accounts below to explore the system based on different roles.

### Employee

This username and password is also for the super user, able to login into admin panel

- Username: `meimei`

- Password: `employee`

### Instructor

- Username: `Rebecca`

- Password: `instructor`

### Student

- Username: `Yoona`

- Password: `students`

## 📷 Demo

- Login page

![login-page](/screenshots/login-page.png)

- Admin dashboard

![admin-dashboard](/screenshots/admin-dashboard.png)

- Instructor dashboard

![instructor-dashboard](/screenshots/instructor-dashboard.png)

- Student dashboard

![student-dashboard](/screenshots/student-dashboard.png)
