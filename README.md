# 🏢 Room Booking System
  
  A virtual workspace room booking API using Django Rest Framework.

## 🧠 Overview

This RESTful API simulates a shared office environment where users and teams can book rooms and desks based on predefined rules and constraints.

## 🚀 Features

- 🧍 Private room booking for individual users
- 👥 Conference rooms for teams (3+ members)
- 🪑 Shared desks auto-fill until full (4 users/desk)
- ⏱️ Time slots: 9 AM – 6 PM (hourly)
- ✅ Validation rules for overlapping bookings and slot logic
- 🧪 Unit testing with `pytest`
- 📘 Swagger (drf-yasg) documentation

## 🛠 Tech Stack

- Python 
- Django
- Django REST Framework
- PostgreSQL
- Swagger


## 🔧 Getting Started

### Clone the repository
```bash
git clone https://github.com/jsnehi/room-booking-system.git
cd room-booking-system
```

### Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Apply migrations
```bash
python manage.py migrate
```

### Run development server
```bash
python manage.py runserver
```

## 📘 API Documentation
After starting the server, visit:

```bash
http://localhost:8000/api/docs
```
