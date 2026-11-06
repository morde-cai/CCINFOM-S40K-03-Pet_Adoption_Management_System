# Paws 
> A Pet Adoption Management System

**Paws** helps shelters manage their pets, staff, adopters, and adoption requests in one place. It provides a centralized platform for tracking pet records, managing adoption processes, maintaining staff and adopter information, and generating reports on shelter activities.

<!-- Yo guys let's add an image here once we're done lol -->



## Table of Contents

- [Paw Patrol Members](#paw-patrol-members)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Design (ERD)](#database-design-erd)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [References](#references)


## Paw Patrol Members

**Section & Group Number:** S40K - 03  
**School:** De La Salle University Manila  
**Course:** CCINFOM | A.Y. 2026 - 2027 Term 1  
**Instructor:** Dr. Payawal, Bryan O’Nomerp  

| Name | Role / Contribution |
|------|---------------------|
| Aceveda, Jiahe    | DB Design, `TODO` |
| Dy, Jasmine       | DB Design, `TODO` |
| Nucum, Mark       | DB Design, `TODO` |
| Pielago, James C. | DB Design, Backend Development, Core Features, Documentation |



## Features
`TODO`

### Record Management

Each of the main records supports the standard record management functions:

- Create a new record.
- Read/View an existing record.
- Update an existing record.
- Delete an existing record.
- List records, filterable by a set of fields.

Managed records:

- **Pets** (with photos)
- **Breeds** and **Species**
- **Adopters** (stored as records, entered and maintained by staff)
- **Staff** and **Staff Roles**
- **Adoptions**
- **Shelters**


## Tech Stack
`TODO`


## Database Design (ERD)
`TODO`


## Getting Started
Follow the guide step-by-step.

### Prerequisites

- [`TODO`](link)
- [`TODO`](link)

### 1. Clone the repository
Use this repository's URL.

```bash
# (Optional) Change to preferred folder
cd [your_folder]

# Clone
git clone [URL]

# Change to the repository folder
cd CCINFOM-S40K-03-Pet_Adoption_Management_System
```

### 2. Create and activate a virtual environment
Creation is only once; activation is for every use.
```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS / Linux)
source venv/bin/activate
```

### 3. Install dependencies
Once your `venv` is activated, install the dependencies.
```bash
# Change directory
cd pet_adoption_system

# Then run:
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy the example file to create your own `.env` (same folder as `manage.py`):

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Then open `.env` and fill in your own values. **Never commit this file.** It should already be in your `.gitignore`.
```py
SECRET_KEY=your-own/generated-key # Change for actual use
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=

DB_ENGINE=django.db.backends.mysql
DB_NAME=pet_adoption_db
DB_USER=petuser
DB_PASSWORD=your_mysql_password # Change to actual password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Make your own `SECRET_KEY` or generate one:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

> Copy the key into your `.env`. No quotes around values and no spaces around the `=` in `.env`.

### 5. Set up the database
Log in your MySQL account (ensure your MySQL is in your Environmental Variables Path):
```bash
mysql -u root -p
```

Then run to create the database in MySQL:
> Change to your password
```sql
CREATE DATABASE IF NOT EXISTS pet_adoption_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'petuser'@'localhost'
IDENTIFIED BY 'your_password_here';
GRANT ALL PRIVILEGES ON pet_adoption_db.* TO 'petuser'@'localhost';
EXIT;
```

### 6. Run migrations
These allow us to let Django prepare the models and actually apply them into the MySQL db. 
Redo this to apply any change you made to the models. 
```bash
python manage.py makemigrations
python manage.py migrate
```

### `TODO` 7. (Optional) Load sample data 

```bash
python manage.py loaddata [fixture_file].json
```

### 8. Create an admin account

```bash
python manage.py createsuperuser
```

### 9. Run the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser or whatever is your host in the terminal.


## Project Structure
`TODO`


## Screenshots
`TODO`


## References
- *AmaneKai (n.d.). CCINFOM-DBAPP-SAMPLE. https://github.com/AmaneKai/CCINFOM-DBAPP-SAMPLE*
- *Django (n.d.). Django documentation. Django Project. https://docs.djangoproject.com/en/6.1/*
- *Bootstrap (n.d.). Bootstrap 6 Documentation. https://getbootstrap.com/docs/6.0/getting-started/install/*
- *Lucide (n.d.). Lucide. https://lucide.dev/*
- *Chart.js (n.d.). Chart.js Docs. https://www.chartjs.org/docs/latest/*