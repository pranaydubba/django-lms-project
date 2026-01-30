# Django Learning Management System (LMS)

This project is a web-based Learning Management System built using Django and PostgreSQL. It supports student and instructor roles, where instructor can manage courses by adding and editing course contents. Wheareas Students can enroll courses and view lessons and attend quizzes thereby tracking course progress.

## 🚀 Features

- User authentication and role-based access (Student / Instructor)
- Admin's approval for Instructor's login
- Course creation and management
- Student enrollments
- Section-wise course content
- Quizzes with questions and results
- Student and instructor dashboards
- Users can edit their profiles and change Password
- Responsive UI using HTML, CSS and JavaScript

---

## 🛠️ Tech Stack

- Backend: Django (Python)
- Database: PostgreSQL
- Frontend: HTML, CSS ,JavaScript
- Version Control: Git & GitHub

---

## 📁 Project Structure

├── accounts/
├── courses/
├── dashboard/
├── enrollments/
├── quizzes/
├── lms_proj/ # Main Django project settings
├── templates/
├── static/
│ └── css/
├── manage.py
├── .gitignore

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/pranaydubba/django-lms-project.git
cd django-lms-project
```

### 2️⃣ Create and activate virtual environment

python -m venv venv
venv\Scripts\activate   # Windows

source venv/bin/activate   # Linux/Mac
