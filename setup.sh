#!/bin/bash

echo "🐾 Setting up PetFoodHub Meals..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

echo "✅ Dependencies installed"

# Run migrations
python manage.py migrate

echo "✅ Database migrated"

# Create superuser
echo "Creating admin user..."
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --no-input

echo "🎉 Setup complete!"
echo "Run 'python manage.py runserver' to start the development server"
```

Make executable:
```bash
chmod +x setup.sh