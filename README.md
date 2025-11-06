<<<<<<< HEAD
# PetFoodHub

A Django web application that provides personalized dog food recommendations with calculated portions and affiliate shopping links.

## Features

- Personalized meal plans that calculate exact portions based on a dog's weight, age, and activity level  
- Curated meal options from trusted brands with affiliate purchase links  
- User profiles to manage multiple pets and saved meal plans  
- 45-day shopping lists with quantity and cost breakdowns  
- Educational content covering nutrition, portion sizing, and food transitions  
- Admin panel for managing products, meals, and educational articles  

## Tech Stack

- **Backend:** Django 4.2, Python 3.11  
- **Database:** PostgreSQL (production), SQLite (development)  
- **Frontend:** Bootstrap 5, Vanilla JavaScript  
- **Deployment:** Render.com  
- **Static Files:** Whitenoise  

## Local Development Setup

### Prerequisites
- Python 3.11+
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bryanpsullivan/PetFoodHub-Affiliate-Website.git
   cd PetFoodHub-Affiliate-Website
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# or
source venv/bin/activate   # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run database migrations**
```bash
python manage.py migrate
```

5. **Create superuser (for admin access)**
```bash
python manage.py createsuperuser
```

6. **Load initial data (optional)**
```bash
python manage.py loaddata initial_data.json
```

7. **Run development server**
```bash
python manage.py runserver
=======
# PetFoodHub-Affiliate-Website
Affiliate Marketing Website to make finding pet food meal plans easy and affordable using links to Chewy.com. This allows for variety, proper nutrition, and an easy to follow guide to improve your pets diet.
>>>>>>> 60887c5496d4bb1a98ff7b6c2f0b9773d4553ed4
