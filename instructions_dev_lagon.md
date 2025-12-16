# Instructions pour le Développeur - Projet Le Lagon

## 📋 Brief du Projet

**Client :** Restaurant Le Lagon  
**Type :** Site vitrine moderne avec réservation en ligne  
**Liberté créative :** Totale sur le design (dans le thème maritime/lagon)  
**Deadline :** [À définir selon planning 22 jours]

---

## 🎯 Objectifs Prioritaires

### Must-Have (Obligatoire)
1. **Site vitrine élégant** qui donne envie de venir au restaurant
2. **Menu interactif** - navigation fluide, filtres, recherche
3. **Système de réservation fonctionnel** - disponibilité temps réel
4. **Panel admin complet** - le client doit tout gérer seul
5. **100% Responsive** - mobile first
6. **Performance optimale** - chargement rapide

### Nice-to-Have (Si temps disponible)
- Galerie photos avec lightbox
- Témoignages clients en carrousel
- Animations sophistiquées (parallax, etc.)
- Multi-langues (FR/EN)
- Mode sombre

---

## 🛠️ Stack Technique Imposée

### Backend
```
Flask 3.0+
Flask-SQLAlchemy
Flask-Login
Flask-WTF
Flask-Mail
Flask-Migrate
APScheduler
```

### Frontend
```
HTMX 1.9+
TailwindCSS 3.4+
Alpine.js (micro-interactions)
Swiper.js (carrousels)
AOS (animations scroll)
```

### Base de Données
```
PostgreSQL (production)
SQLite (développement local OK)
```

---

## 📁 Structure Projet Imposée

```
le-lagon/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes/
│   │   ├── main.py          # Routes publiques
│   │   ├── reservations.py  # Système réservation
│   │   ├── admin.py         # Panel admin
│   │   └── api.py           # Endpoints HTMX
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── menu.html
│   │   ├── reservation.html
│   │   ├── contact.html
│   │   ├── admin/           # Templates admin
│   │   └── components/      # Fragments HTMX
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── utils/
├── migrations/
├── tests/
├── config.py
├── requirements.txt
├── tailwind.config.js
├── .env.example
└── run.py
```

**⚠️ Respecte cette structure pour la maintenabilité**

---

## 🎨 Design & UX

### Charte Graphique
**Thème : Lagon / Océan / Fraîcheur**

**Palette suggérée :**
- Bleu turquoise : `#00B4D8` (primaire)
- Bleu marine : `#023E8A` (secondaire)
- Corail/Orange : `#FF6B6B` (accents)
- Blanc cassé : `#F8F9FA` (backgrounds)
- Gris foncé : `#2B2D42` (textes)

**Tu es libre d'ajuster** selon ton inspiration, mais garde une identité maritime/lagon.

### Typographie Recommandée
- **Titres :** Playfair Display ou Montserrat (élégant)
- **Corps :** Inter ou Open Sans (lisible)
- Via Google Fonts

### Principes UX
- **Mobile First** - design d'abord pour mobile
- **Navigation intuitive** - max 3 clics pour toute action
- **CTA visibles** - "Réserver" doit être évident partout
- **Chargement rapide** - images optimisées, lazy loading
- **Accessibilité** - contraste WCAG AA minimum

### Inspirations
- Sites de restaurants gastronomiques modernes
- Airbnb pour le système de réservation
- Uber Eats pour le menu interactif

---

## 🔥 Fonctionnalités Détaillées

### 1. Page d'Accueil
**Sections requises :**
- Hero immersif (image/vidéo + CTA "Réserver")
- Présentation restaurant (3-4 paragraphes)
- Aperçu menu (3-4 plats phares avec photos)
- Galerie photos (ambiance, plats, équipe)
- Témoignages clients (3-5 avis)
- Localisation + horaires
- Footer complet (contact, réseaux sociaux, mentions légales)

**Interactions HTMX :**
- Chargement lazy des images galerie
- Carrousel témoignages sans rechargement

---

### 2. Menu Interactif (Priorité Haute)

**Fonctionnalités obligatoires :**
- ✅ Catégories : Entrées, Plats, Desserts, Boissons
- ✅ Filtres dynamiques HTMX :
  - Par catégorie
  - Par régime (végétarien, vegan, sans gluten)
  - Par allergènes
- ✅ Barre de recherche temps réel (HTMX)
- ✅ Toggle vue grille / liste (Alpine.js)
- ✅ Chaque plat affiche :
  - Photo de qualité
  - Nom + description
  - Prix
  - Badges (nouveauté, spécialité, épicé)
  - Allergènes
- ✅ Modal détails plat au clic

**Exemple HTMX :**
```html
<form hx-post="/api/menu/filter" 
      hx-target="#menu-results" 
      hx-trigger="change">
  <select name="category">...</select>
  <input type="search" name="query" 
         hx-trigger="keyup changed delay:500ms">
</form>
```

**Données initiales :**
Je te fournirai 15-20 plats exemples avec photos, ou utilise des placeholders Unsplash en attendant.

---

### 3. Système de Réservation (Priorité Critique)

**Workflow utilisateur :**
1. Sélection date (calendrier interactif - Flatpickr)
2. Sélection heure (créneaux disponibles seulement)
3. Nombre de personnes (2-10)
4. **Vérification disponibilité en temps réel** (HTMX)
5. Formulaire coordonnées :
   - Nom, Prénom
   - Email
   - Téléphone
   - Demandes spéciales (optionnel)
6. Confirmation visuelle
7. Email automatique (client + restaurant)

**Règles métier IMPORTANTES :**
- Service midi : 12h00 - 14h30
- Service soir : 19h00 - 22h30
- Créneaux toutes les 30 minutes
- Capacité totale : 50 personnes simultanées
- Durée table : 2h (automatique)
- Pas de réservation < 2h avant le service
- Pas de réservation > 2 mois à l'avance
- Fermeture : Lundis (configurable admin)

**Endpoint HTMX disponibilité :**
```python
@api.route('/check-availability', methods=['POST'])
def check_availability():
    date = request.form.get('date')
    time = request.form.get('time')
    guests = request.form.get('guests')
    
    # Logique vérification
    available_slots = calculate_slots(date, time, guests)
    
    # Retourne fragment HTML
    return render_template('components/slots.html', 
                         slots=available_slots)
```

**Emails automatiques :**
- Confirmation immédiate client
- Notification restaurant
- Rappel 24h avant (APScheduler)
- Template HTML responsive

---

### 4. Panel Administrateur (Priorité Haute)

**URL :** `/admin` (sécurisé Flask-Login)

#### Dashboard
- 📊 Réservations du jour (tableau)
- 📈 Statistiques :
  - Taux de remplissage semaine
  - Réservations à venir
  - Graphique fréquentation (Chart.js)
- 🔔 Alertes (réservations non confirmées)

#### Gestion Réservations
**Liste filtrable :**
- Par date (range picker)
- Par statut (en attente, confirmé, annulé, terminé)
- Par nom client (recherche)

**Actions HTMX :**
- ✅ Confirmer (change statut)
- ❌ Annuler (modal confirmation)
- ✏️ Modifier (heure, nb personnes)
- 📝 Ajouter note interne
- 📥 Export CSV

**Interface :**
Table responsive avec actions inline (boutons HTMX).

#### Gestion Menu
**CRUD complet :**
- ➕ Ajouter plat (formulaire modal)
- ✏️ Modifier plat (inline editing ou modal)
- 🗑️ Supprimer plat (confirmation)
- 📸 Upload photo (drag & drop)
- 🔄 Réorganiser ordre (drag & drop - SortableJS)
- 👁️ Activer/désactiver disponibilité

**Formulaire plat :**
```
- Nom*
- Catégorie* (dropdown)
- Description*
- Prix*
- Photo (upload)
- Allergènes (multi-select)
- Régimes (checkboxes: vegan, gluten-free...)
- Badges (nouveauté, spécialité...)
- Disponible (toggle)
```

#### Configuration
- Horaires d'ouverture (par jour)
- Jours de fermeture exceptionnelle
- Capacité restaurant
- Durée moyenne table
- Paramètres réservation (délai min/max)
- Coordonnées restaurant
- Emails notifications

**Stockage :** Table `settings` (key-value)

---

### 5. Page Contact
- Formulaire simple :
  - Nom, Email, Téléphone, Message
  - Protection CSRF
  - Validation côté serveur
- Envoi email automatique
- Carte interactive (Google Maps ou Leaflet + OpenStreetMap)
- Coordonnées complètes
- Liens réseaux sociaux
- Horaires

---

## 🔐 Sécurité (Non Négociable)

### Implémentations Obligatoires
1. **CSRF Protection** - Flask-WTF sur tous les formulaires
2. **Validation stricte** - côté serveur (never trust client)
3. **SQL Injection** - utilise ORM uniquement (pas de raw SQL)
4. **XSS Protection** - escape tous les outputs (`{{ var | e }}`)
5. **Rate Limiting** - Flask-Limiter :
   - Login : 5 tentatives / 15 min
   - Contact : 3 envois / heure
   - Réservation : 5 / heure
6. **Passwords** - hachage Werkzeug (jamais en clair)
7. **Variables sensibles** - `.env` JAMAIS committé
8. **HTTPS** - obligatoire en production
9. **Headers sécurité** - Flask-Talisman

### .env.example à créer
```env
SECRET_KEY=change-me-in-production
DATABASE_URL=postgresql://user:pass@localhost/lelagon
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
ADMIN_EMAIL=admin@lelagon.com
```

---

## 📱 Responsive Design

### Breakpoints TailwindCSS
- **sm:** 640px (mobile paysage)
- **md:** 768px (tablette)
- **lg:** 1024px (desktop)
- **xl:** 1280px (grand écran)

### Tests Obligatoires
- ✅ iPhone SE (375px)
- ✅ iPhone 12 Pro (390px)
- ✅ iPad (768px)
- ✅ Desktop 1920px

### Règles
- Menu burger sur mobile/tablette
- Images responsive (srcset ou TailwindCSS)
- Touch-friendly (min 44x44px boutons)
- Formulaires optimisés mobile

---

## ⚡ Performance

### Optimisations Requises
1. **Images :**
   - Format WebP avec fallback JPG
   - Lazy loading (loading="lazy")
   - Compression Pillow (qualité 85%)
   - Responsive images
   
2. **CSS/JS :**
   - TailwindCSS purgé (production)
   - Minification
   - Defer non-critical JS
   
3. **Cache :**
   - Flask-Caching sur pages statiques
   - Cache-Control headers
   - Browser caching (1 an assets)
   
4. **Base de données :**
   - Index sur colonnes fréquentes (date, email)
   - Lazy loading relations SQLAlchemy

### Objectif PageSpeed
- **Mobile :** > 80
- **Desktop :** > 90

---

## 🧪 Tests & Qualité

### Tests Unitaires (pytest)
Minimum requis :
- Models (création, validation)
- Réservation (disponibilité, conflits)
- Filtres menu
- Authentification admin

### Tests d'Intégration
- Workflow réservation complet
- CRUD admin
- Envoi emails

### Code Quality
- **Black** - formatage automatique
- **Flake8** - linting (max-line-length 100)
- **Type hints** - sur fonctions critiques
- **Docstrings** - fonctions publiques

### Commandes
```bash
pytest tests/
black app/
flake8 app/
```

---

## 📊 SEO (Obligatoire)

### Meta Tags par Page
```html
<title>Le Lagon - Restaurant [Page] | Ville</title>
<meta name="description" content="...">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="...">
<meta property="og:type" content="website">
```

### Implémentations
1. **Sitemap.xml** - auto-généré (Flask-Sitemap)
2. **Robots.txt** - autoriser tout sauf /admin
3. **Schema.org** - markup Restaurant + Menu
```json
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "Le Lagon",
  "address": {...},
  "servesCuisine": "Française",
  "priceRange": "$$"
}
```
4. **Alt text** - toutes les images
5. **Heading hierarchy** - H1 unique par page
6. **URLs propres** - `/menu/entrees` pas `/menu?cat=1`

---

## 🚀 Déploiement

### Environnement de Production

**Option recommandée : VPS (DigitalOcean / Hetzner)**

Stack serveur :
```
Ubuntu 22.04 LTS
Nginx (reverse proxy)
Gunicorn (WSGI server)
PostgreSQL
Supervisor (process management)
Let's Encrypt (SSL)
```

### Configuration Nginx
```nginx
server {
    listen 80;
    server_name lelagon.com www.lelagon.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /var/www/lelagon/app/static;
        expires 1y;
    }
}
```

### Déploiement Script
Fournis un `deploy.sh` :
```bash
#!/bin/bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
sudo supervisorctl restart lelagon
```

### Variables Environnement Production
```env
FLASK_ENV=production
DATABASE_URL=postgresql://...
SECRET_KEY=[généré aléatoirement]
MAIL_SERVER=...
```

---

## 📦 Livrables Attendus

### Code
- ✅ Repository Git (GitHub/GitLab)
- ✅ Commits réguliers (messages clairs)
- ✅ Branches (main, develop)
- ✅ .gitignore propre
- ✅ requirements.txt complet

### Documentation
- ✅ README.md :
  - Installation locale
  - Configuration .env
  - Commandes utiles
  - Structure projet
- ✅ DEPLOYMENT.md :
  - Instructions serveur production
  - Configuration Nginx
  - Gestion backups
- ✅ ADMIN_GUIDE.md :
  - Guide utilisation panel admin
  - Captures d'écran
  - FAQ

### Assets
- ✅ Compte admin par défaut :
  - Username : `admin`
  - Password : `ChangeMeNow123!`
- ✅ Données démo (20 plats minimum)
- ✅ 3-5 réservations exemples

### Tests
- ✅ Suite tests complète
- ✅ Coverage > 70%
- ✅ CI/CD basique (GitHub Actions)

---

## 📅 Planning & Jalons

### Phase 1 : Setup (Jours 1-3)
**Livrables :**
- Structure projet complète
- Base de données + migrations
- Config Flask + Tailwind compilé
- Template base responsive

**Validation :** Projet run en local, navigation basique fonctionne

---

### Phase 2 : Frontend Public (Jours 4-8)
**Livrables :**
- Page accueil complète
- Menu interactif avec filtres HTMX
- Page contact fonctionnelle
- Design responsive finalisé

**Validation :** Site navigable, design approuvé

---

### Phase 3 : Réservation (Jours 9-13)
**Livrables :**
- Calendrier interactif
- Vérification disponibilité temps réel
- Workflow complet réservation
- Emails automatiques
- Tests unitaires

**Validation :** Réservation end-to-end fonctionne, emails reçus

---

### Phase 4 : Panel Admin (Jours 14-17)
**Livrables :**
- Authentification sécurisée
- Dashboard avec stats
- CRUD réservations
- CRUD menu
- Configuration

**Validation :** Admin peut gérer tout le site

---

### Phase 5 : Optimisation (Jours 18-20)
**Livrables :**
- SEO complet (meta, sitemap, schema)
- Optimisation images
- Cache + compression
- Tests cross-browser
- Accessibilité validée

**Validation :** PageSpeed > 80, tests passent

---

### Phase 6 : Déploiement (Jours 21-22)
**Livrables :**
- Site en ligne sur serveur production
- SSL configuré
- Backups automatiques
- Documentation complète
- Passation client

**Validation :** Site live, client formé

---

## 🆘 Support & Communication

### Outils de Communication
- **Daily standup :** 15 min / jour (Zoom/Meet)
- **Slack/Discord :** Messages asynchrones
- **Trello/Notion :** Suivi tâches
- **GitHub Issues :** Bugs & features

### Points de Validation
- **Fin de chaque phase :** Démo + validation
- **Blockers :** Signaler immédiatement
- **Questions design :** Screenshots + alternatives

### Contact Client
- Disponible pour questions : [horaires]
- Délai réponse max : 24h ouvrées
- Validation design : 48h max

---

## ⚠️ Points de Vigilance

### Pièges à Éviter
1. **Over-engineering** - reste simple et pragmatique
2. **Scope creep** - fonctionnalités non spécifiées = à valider avant
3. **Pas de tests** - coûte plus cher à corriger après
4. **Sécurité négligée** - données clients sensibles
5. **Mobile oublié** - 60%+ trafic mobile
6. **Performance ignorée** - slow site = bounce rate élevé

### Questions à Poser AVANT de Coder
- Cette fonctionnalité est-elle dans le scope ?
- Ai-je tous les assets nécessaires ?
- Cette dépendance est-elle maintenue ?
- Comment tester ce comportement ?
- Qu'est-ce qui peut casser en production ?

---

## 📞 Contacts & Ressources

### Documentation Technique
- Flask : https://flask.palletsprojects.com/
- HTMX : https://htmx.org/docs/
- TailwindCSS : https://tailwindcss.com/docs
- Alpine.js : https://alpinejs.dev/

### Assets Design
- Icônes : Heroicons (https://heroicons.com/)
- Images : Unsplash (https://unsplash.com/)
- Illustrations : unDraw (https://undraw.co/)

### Contact Projet
- **Client :** [Nom + Email + Téléphone]
- **Chef de Projet :** [Nom + Contact]
- **Budget :** [X jours/homme à Y€]

---

## ✅ Checklist Finale Avant Livraison

### Fonctionnel
- [ ] Toutes les pages sont accessibles
- [ ] Menu interactif fonctionne (filtres, recherche)
- [ ] Réservation complète (de A à Z)
- [ ] Emails de confirmation envoyés
- [ ] Panel admin accessible et fonctionnel
- [ ] CRUD réservations opérationnel
- [ ] CRUD menu opérationnel
- [ ] Formulaire contact fonctionne

### Qualité
- [ ] Responsive sur tous devices
- [ ] Cross-browser (Chrome, Firefox, Safari, Edge)
- [ ] Pas d'erreurs console
- [ ] Tests unitaires passent
- [ ] Coverage > 70%
- [ ] Code formaté (Black)
- [ ] Linting OK (Flake8)

### Performance
- [ ] PageSpeed Mobile > 80
- [ ] PageSpeed Desktop > 90
- [ ] Images optimisées
- [ ] Cache configuré
- [ ] Lazy loading images

### Sécurité
- [ ] CSRF protection active
- [ ] Rate limiting configuré
- [ ] Variables sensibles en .env
- [ ] HTTPS en production
- [ ] Headers sécurité (Talisman)
- [ ] Validation inputs serveur

### SEO
- [ ] Meta tags toutes pages
- [ ] Sitemap.xml généré
- [ ] Robots.txt configuré
- [ ] Schema.org markup
- [ ] Alt text images
- [ ] URLs propres

### Documentation
- [ ] README.md complet
- [ ] Guide déploiement
- [ ] Guide admin
- [ ] Commentaires code
- [ ] .env.example fourni

### Déploiement
- [ ] Site live production
- [ ] SSL configuré
- [ ] Backups automatiques
- [ ] Monitoring actif
- [ ] Logs accessibles

---

## 🎉 Notes Finales

**Philosophie du Projet :**
- **Qualité > Quantité** - un site parfaitement exécuté vaut mieux qu'un site bourré de features buggées
- **User First** - toujours penser à l'expérience client final
- **Maintenabilité** - code propre = client autonome
- **Communication** - signaler les blockers rapidement

**Liberté Créative :**
Tu as carte blanche sur :
- Design visuel (respecte le thème lagon)
- Animations et transitions
- Micro-interactions
- Layout exact des pages

**Attentes Client :**
Un site qui fait dire "Wow, je veux réserver !" 🌊

**Bon développement ! 🚀**

---

*Document créé pour le projet Le Lagon*  
*Version 1.0 - Décembre 2024*