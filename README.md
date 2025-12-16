# Le Lagon - Restaurant Website

Site vitrine moderne pour le restaurant "Le Lagon" avec système de réservation en ligne et menu interactif.

## Stack Technique

- **Backend**: Flask 3.0+, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Mail
- **Frontend**: HTMX, TailwindCSS, Alpine.js, Swiper.js, AOS
- **Base de données**: SQLite (dev) / PostgreSQL (production)

## Installation

### 1. Créer un environnement virtuel

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer l'environnement

Copier `.env.example` vers `.env` et configurer les variables:
```bash
copy .env.example .env
```

### 4. Initialiser la base de données

```bash
set FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Charger les données de démonstration

```bash
python seed_data.py
```

### 6. Compiler Tailwind CSS (optionnel, un fichier pré-compilé est inclus)

```bash
npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/output.css --watch
```

### 7. Lancer l'application

```bash
flask run
```

L'application sera accessible à http://localhost:5000

## Comptes par défaut

- **Admin**: 
  - Email: `admin@lelagon.com`
  - Mot de passe: `ChangeMeNow123!`

## Structure du projet

```
le-lagon/
├── app/
│   ├── __init__.py       # Factory Flask
│   ├── models.py         # Modèles SQLAlchemy
│   ├── forms.py          # Formulaires WTForms
│   ├── routes/           # Blueprints (main, reservations, admin, api)
│   ├── templates/        # Templates Jinja2
│   ├── static/           # CSS, JS, images
│   └── utils/            # Utilitaires
├── migrations/           # Migrations Alembic
├── tests/                # Tests unitaires
├── config.py             # Configuration
├── run.py                # Point d'entrée
├── seed_data.py          # Script de seed
└── requirements.txt      # Dépendances
```

## Pages

- `/` - Accueil
- `/menu` - Carte interactive
- `/reservation` - Réservation en ligne
- `/contact` - Contact
- `/admin/login` - Connexion admin
- `/admin/dashboard` - Dashboard admin

## Développement

### Linting & Formatage
```bash
black app/
flake8 app/
```

### Tests
```bash
pytest tests/
```

## Déploiement

Voir `DEPLOYMENT.md` pour les instructions de déploiement en production.

---
*Le Lagon - Saveurs Marines entre Ciel et Mer*
