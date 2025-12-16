# Cahier des Charges - Site Vitrine Restaurant Le Lagon

## 1. Présentation du Projet

### 1.1 Contexte
Création d'un site vitrine moderne pour le restaurant "Le Lagon" avec système de réservation en ligne et menu interactif.

### 1.2 Objectifs
- Présenter l'établissement et son identité
- Afficher le menu de manière attractive et interactive
- Permettre les réservations en ligne 24/7
- Optimiser la visibilité sur les moteurs de recherche
- Offrir une expérience utilisateur fluide et moderne

---

## 2. Stack Technique

### 2.1 Backend
- **Flask 3.0+** : Framework web Python léger et flexible
- **Flask-SQLAlchemy** : ORM pour la gestion de base de données
- **Flask-Login** : Gestion des sessions administrateur
- **Flask-WTF** : Gestion des formulaires avec protection CSRF
- **Flask-Mail** : Envoi d'emails (confirmations de réservation)
- **Flask-Migrate** : Migrations de base de données (Alembic)
- **APScheduler** : Tâches planifiées (rappels, nettoyage)

### 2.2 Frontend
- **HTMX 1.9+** : Interactions dynamiques sans JavaScript complexe
- **TailwindCSS 3.4+** : Framework CSS utility-first
- **Alpine.js 3.x** : JavaScript léger pour micro-interactions
- **Swiper.js** : Carrousels d'images fluides
- **AOS (Animate On Scroll)** : Animations au scroll

### 2.3 Base de Données
- **PostgreSQL** (production) : Robuste et scalable
- **SQLite** (développement) : Simplicité locale

### 2.4 Outils Complémentaires
- **Pillow** : Traitement d'images (redimensionnement, optimisation)
- **python-dotenv** : Gestion des variables d'environnement
- **Gunicorn** : Serveur WSGI pour production
- **Nginx** : Reverse proxy et serveur de fichiers statiques
- **Redis** : Cache et gestion de sessions (optionnel mais recommandé)

### 2.5 Qualité & Tests
- **pytest** : Tests unitaires et d'intégration
- **Black** : Formatage automatique du code
- **Flake8** : Linting Python

---

## 3. Architecture du Projet

```
le-lagon/
├── app/
│   ├── __init__.py
│   ├── models.py              # Modèles de données
│   ├── forms.py               # Formulaires WTForms
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py            # Routes publiques
│   │   ├── reservations.py   # Gestion réservations
│   │   ├── admin.py           # Panel administrateur
│   │   └── api.py             # Endpoints HTMX
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── menu.html
│   │   ├── reservation.html
│   │   ├── contact.html
│   │   ├── admin/
│   │   └── components/        # Fragments HTMX
│   ├── static/
│   │   ├── css/
│   │   │   └── output.css     # Tailwind compilé
│   │   ├── js/
│   │   │   └── main.js
│   │   └── images/
│   └── utils/
│       ├── email.py           # Envoi emails
│       ├── validators.py      # Validations custom
│       └── helpers.py         # Fonctions utilitaires
├── migrations/                # Migrations Alembic
├── tests/
├── config.py                  # Configuration Flask
├── requirements.txt
├── tailwind.config.js
├── .env.example
└── run.py                     # Point d'entrée
```

---

## 4. Fonctionnalités Détaillées

### 4.1 Page d'Accueil
**Éléments :**
- Hero section avec image/vidéo immersive
- Présentation du restaurant (histoire, concept)
- Galerie photos (plats, ambiance, équipe)
- Témoignages clients (carrousel)
- Horaires et localisation
- Call-to-action vers réservation

**Techniques :**
- Lazy loading des images (Pillow pour optimisation)
- Animations AOS au scroll
- Carrousel Swiper.js pour galerie
- Section map avec intégration Google Maps ou OpenStreetMap

### 4.2 Menu Interactif
**Fonctionnalités :**
- Catégories (Entrées, Plats, Desserts, Boissons)
- Filtres dynamiques (végétarien, sans gluten, épicé)
- Recherche en temps réel (HTMX)
- Fiches détaillées par plat :
  - Photo haute qualité
  - Description
  - Allergènes
  - Prix
  - Badge "Spécialité" / "Nouveauté"
- Mode vue grille / liste

**Techniques :**
- HTMX pour filtrage sans rechargement
- Alpine.js pour toggle grille/liste
- Images WebP avec fallback
- Modal lightbox pour détails plats

### 4.3 Système de Réservation
**Workflow :**
1. Sélection date/heure via calendrier interactif
2. Choix nombre de personnes
3. Vérification disponibilité en temps réel (HTMX)
4. Formulaire coordonnées client
5. Confirmation avec email automatique
6. SMS de rappel 24h avant (optionnel - Twilio)

**Règles de Gestion :**
- Plages horaires configurables (service midi/soir)
- Capacité maximale par créneau
- Durée moyenne par table (2h par défaut)
- Blocage des réservations < 2h avant le service
- Système d'overbooking contrôlé (10% de marge)
- Gestion des annulations jusqu'à 12h avant

**Techniques :**
- Flatpickr.js pour datepicker avancé
- HTMX pour check disponibilité asynchrone
- Flask-Mail pour confirmations
- APScheduler pour rappels automatiques
- Stockage réservations en BDD avec statuts (pending, confirmed, completed, cancelled)

### 4.4 Panel Administrateur
**Accès :**
- Page login sécurisée (/admin/login)
- Flask-Login pour authentification
- Middleware admin_required

**Fonctionnalités :**
- **Dashboard :**
  - Réservations du jour
  - Statistiques (taux de remplissage, CA prévisionnel)
  - Graphiques de fréquentation (Chart.js)
  
- **Gestion Réservations :**
  - Liste filtrable (date, statut, nom)
  - Actions : valider, annuler, modifier
  - Notes internes par réservation
  - Export CSV

- **Gestion Menu :**
  - CRUD complet plats/catégories
  - Upload photos (drag & drop)
  - Gestion stocks/disponibilité
  - Activation/désactivation plats

- **Configuration :**
  - Horaires d'ouverture
  - Jours de fermeture
  - Capacité par créneau
  - Paramètres réservation

**Techniques :**
- HTMX pour actions CRUD sans rechargement
- TailwindCSS pour interface moderne
- Flask-WTF pour formulaires sécurisés
- Pagination côté serveur

### 4.5 Page Contact
- Formulaire de contact (email automatique)
- Coordonnées complètes
- Carte interactive
- Liens réseaux sociaux
- Horaires d'ouverture

### 4.6 SEO & Performance
- Meta tags dynamiques par page
- Open Graph pour réseaux sociaux
- Sitemap.xml auto-généré
- Robots.txt
- Schema.org markup (Restaurant, Menu)
- Compression Gzip
- Mise en cache statique (Flask-Caching)
- CDN pour assets (optionnel)

---

## 5. Modèles de Données

### 5.1 Reservation
```python
- id: Integer (PK)
- date: Date
- time: Time
- guests: Integer
- first_name: String(100)
- last_name: String(100)
- email: String(120)
- phone: String(20)
- status: Enum (pending, confirmed, completed, cancelled)
- special_requests: Text
- created_at: DateTime
- updated_at: DateTime
```

### 5.2 MenuItem
```python
- id: Integer (PK)
- name: String(150)
- category_id: Integer (FK)
- description: Text
- price: Decimal(10, 2)
- image_url: String(255)
- allergens: String(255)
- dietary_tags: String(100) # vegan, gluten-free...
- is_available: Boolean
- is_special: Boolean
- order: Integer
- created_at: DateTime
```

### 5.3 Category
```python
- id: Integer (PK)
- name: String(100)
- slug: String(100)
- order: Integer
```

### 5.4 User (Admin)
```python
- id: Integer (PK)
- username: String(80)
- email: String(120)
- password_hash: String(255)
- role: String(20)
- created_at: DateTime
```

### 5.5 Settings
```python
- id: Integer (PK)
- key: String(100) UNIQUE
- value: Text
- updated_at: DateTime
```

### 5.6 Testimonial
```python
- id: Integer (PK)
- author_name: String(100)
- rating: Integer (1-5)
- comment: Text
- is_published: Boolean
- created_at: DateTime
```

---

## 6. API / Endpoints HTMX

### Publics
- `GET /` - Accueil
- `GET /menu` - Menu complet
- `GET /menu/<category>` - Menu par catégorie
- `POST /api/menu/filter` - Filtrage dynamique (HTMX)
- `GET /reservation` - Formulaire réservation
- `POST /api/check-availability` - Vérification dispo (HTMX)
- `POST /reservation/confirm` - Validation réservation
- `GET /contact` - Page contact
- `POST /contact/send` - Envoi message

### Admin
- `GET /admin/login` - Page login
- `POST /admin/login` - Authentification
- `GET /admin/dashboard` - Tableau de bord
- `GET /admin/reservations` - Liste réservations
- `PUT /admin/reservations/<id>` - Modifier réservation (HTMX)
- `DELETE /admin/reservations/<id>` - Annuler (HTMX)
- `GET /admin/menu` - Gestion menu
- `POST /admin/menu/item` - Créer plat (HTMX)
- `PUT /admin/menu/item/<id>` - Modifier plat
- `DELETE /admin/menu/item/<id>` - Supprimer plat
- `GET /admin/settings` - Paramètres

---

## 7. Design & UX

### 7.1 Charte Graphique
**Palette de couleurs (suggestion thème lagon) :**
- Primaire : Bleu turquoise (#00B4D8)
- Secondaire : Bleu marine (#023E8A)
- Accent : Corail (#FF6B6B)
- Neutre : Gris clair (#F8F9FA)
- Texte : Gris foncé (#2B2D42)

**Typographie :**
- Titres : Playfair Display / Montserrat
- Corps : Inter / Open Sans

### 7.2 Responsive Design
- Mobile First
- Breakpoints Tailwind (sm, md, lg, xl, 2xl)
- Menu burger mobile
- Touch-friendly (boutons min 44x44px)

### 7.3 Accessibilité
- Contraste WCAG AA minimum
- Navigation clavier
- Attributs ARIA
- Alt text sur images
- Focus visible

---

## 8. Sécurité

- Protection CSRF (Flask-WTF)
- Validation côté serveur stricte
- Hachage passwords (Werkzeug)
- Rate limiting (Flask-Limiter) sur formulaires
- Sanitization inputs (bleach)
- HTTPS obligatoire en production
- Variables sensibles en .env (SECRET_KEY, DB_URI, MAIL_PASSWORD)
- Headers sécurité (Flask-Talisman)

---

## 9. Déploiement

### 9.1 Environnement de Production
**Option 1 : VPS (DigitalOcean, Linode, Hetzner)**
- Serveur Ubuntu 22.04 LTS
- Nginx + Gunicorn
- PostgreSQL
- SSL/TLS (Let's Encrypt)
- Supervisor pour gestion processus

**Option 2 : PaaS (Heroku, Render, Railway)**
- Déploiement automatisé depuis Git
- PostgreSQL managé
- SSL automatique

### 9.2 CI/CD
- Git workflow (main, develop, feature branches)
- Tests automatiques (pytest)
- Déploiement automatique sur push main

### 9.3 Monitoring
- Logs centralisés
- Uptime monitoring (UptimeRobot)
- Erreurs (Sentry)
- Analytics (Google Analytics / Plausible)

---

## 10. Planning de Développement

### Phase 1 : Setup & Architecture (3 jours)
- Configuration environnement
- Structure projet Flask
- Setup Tailwind + HTMX
- Modèles de données
- Migrations initiales

### Phase 2 : Frontend Public (5 jours)
- Template base + navigation
- Page accueil
- Menu interactif
- Page contact
- Responsive design

### Phase 3 : Système Réservation (5 jours)
- Formulaire réservation
- Logique disponibilité
- Validation + confirmation
- Emails automatiques
- Tests unitaires

### Phase 4 : Panel Admin (4 jours)
- Authentification
- Dashboard
- CRUD réservations
- CRUD menu
- Configuration

### Phase 5 : Optimisation & Tests (3 jours)
- SEO (meta, sitemap)
- Performance (cache, compression)
- Tests d'intégration
- Accessibilité
- Cross-browser testing

### Phase 6 : Déploiement (2 jours)
- Configuration serveur production
- Migration données
- Tests production
- Documentation

**Total estimé : 22 jours**

---

## 11. Livrables

- Code source complet (repository Git)
- Documentation technique
- Guide d'utilisation admin
- Fichiers de configuration
- Scripts de déploiement
- 1 mois de support post-livraison

---

## 12. Maintenance & Évolutions Futures

**Maintenance :**
- Mises à jour sécurité
- Sauvegardes BDD quotidiennes
- Monitoring performances

**Évolutions Possibles :**
- Click & Collect / Livraison
- Programme fidélité
- Newsletter
- Multi-langues (i18n)
- Application mobile (PWA)
- Système de paiement en ligne
- Avis clients vérifiés
- Chatbot (IA pour répondre aux questions)

---

## 13. Budget & Ressources

**Développement :**
- 22 jours développeur senior

**Infrastructure (mensuel) :**
- VPS : ~10-20€/mois
- Nom de domaine : ~15€/an
- SSL : Gratuit (Let's Encrypt)
- Email (SendGrid free tier) : 100 emails/jour gratuit

**Outils :**
- Tous open source (coût 0€)

---

## Annexes

### A. Exemples de Configurations

**requirements.txt :**
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
Flask-Mail==0.9.1
Flask-Migrate==4.0.5
Flask-Limiter==3.5.0
Flask-Caching==2.1.0
python-dotenv==1.0.0
Pillow==10.1.0
APScheduler==3.10.4
psycopg2-binary==2.9.9
gunicorn==21.2.0
email-validator==2.1.0
```

**tailwind.config.js :**
```javascript
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        'lagon-blue': '#00B4D8',
        'lagon-navy': '#023E8A',
        'lagon-coral': '#FF6B6B',
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ]
}
```

### B. Structure HTML de Base avec HTMX

```html
<!-- Exemple filtrage menu -->
<form hx-post="/api/menu/filter" 
      hx-target="#menu-items" 
      hx-trigger="change"
      class="flex gap-4">
  <select name="category">
    <option value="">Toutes catégories</option>
    <option value="entrees">Entrées</option>
    <option value="plats">Plats</option>
  </select>
  <select name="dietary">
    <option value="">Tous</option>
    <option value="vegan">Végétarien</option>
    <option value="gluten-free">Sans gluten</option>
  </select>
</form>

<div id="menu-items">
  <!-- Contenu chargé dynamiquement -->
</div>
```

---

**Document rédigé pour Le Lagon Restaurant**  
*Version 1.0 - Décembre 2024*