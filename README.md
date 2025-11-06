# 🐾 PawPerfect Meals

A Django web application that provides personalized dog food recommendations with calculated portions and affiliate shopping links.

## Features

- **Personalized Meal Plans**: Calculate exact portions based on dog's weight, age, and activity level
- **Smart Recommendations**: Curated meal options from trusted brands
- **User Profiles**: Save multiple pets and their favorite meal plans
- **45-Day Shopping Lists**: Exact quantities needed with cost breakdowns
- **Educational Content**: Guides on nutrition, portions, and food transitions
- **Admin Panel**: Easy product and meal management

## Tech Stack

- **Backend**: Django 4.2, Python 3.11
- **Database**: PostgreSQL (production), SQLite (development)
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Deployment**: Render.com
- **Static Files**: Whitenoise

## Local Development Setup

### Prerequisites
- Python 3.11+
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/pawperfect-meals.git
cd pawperfect-meals
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser (for admin access)**
```bash
python manage.py createsuperuser
```

7. **Load initial data (optional)**
```bash
python manage.py loaddata initial_data.json
```

8. **Run development server**
```bash
python manage.py runserver