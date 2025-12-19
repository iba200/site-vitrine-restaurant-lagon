from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_apscheduler import APScheduler
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)
scheduler = APScheduler()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    # Content Security Policy configuration
    csp = {
        'default-src': ["'self'"],
        'script-src': [
            "'self'",
            "'unsafe-inline'", # Needed for Alpine/AOS inlines if any, sticking to strict might break, but let's allow for now
            "'unsafe-eval'", # Alpine.js often needs this
            "https://unpkg.com",
            "https://cdn.jsdelivr.net"
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'", # Tailwind/AOS often needs this
            "https://fonts.googleapis.com",
            "https://unpkg.com",
            "https://cdn.jsdelivr.net"
        ],
        'font-src': [
            "'self'",
            "https://fonts.gstatic.com"
        ],
        'img-src': [
            "'self'",
            "data:",
            "https:",
            "http:" # Allow loading images from external URLs (unsplash etc)
        ],
         'frame-src': [
            "'self'",
            "https://www.google.com" # For Maps embed
        ]
    }
    
    Talisman(app, 
             content_security_policy=csp, 
             force_https=not app.config.get('DEBUG', True)
    )

    # Register blueprints
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.reservations import reservations as reservations_blueprint
    app.register_blueprint(reservations_blueprint, url_prefix='/reservation')
    
    from .routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    from .routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Inject site-wide settings into templates (safe if DB not ready)
    from .models import Settings

    @app.context_processor
    def inject_site_settings():
        try:
            settings = Settings.get_all() or {}
        except Exception:
            settings = {}

        # Parse some JSON-encoded settings for templates
        import json
        parsed = {}
        for k, v in settings.items():
            if k in ('OPENING_HOURS', 'CLOSED_DATES', 'NOTIFICATION_EMAILS') and v:
                try:
                    parsed[k] = json.loads(v)
                except Exception:
                    parsed[k] = None
            else:
                parsed[k] = v

        # Provide convenient accessors with defaults
        site = {
            'ADDRESS': parsed.get('ADDRESS', ''),
            'PHONE': parsed.get('PHONE', ''),
            'CONTACT_EMAIL': parsed.get('CONTACT_EMAIL', ''),
            'OPENING_HOURS': parsed.get('OPENING_HOURS'),
            'CLOSED_DATES': parsed.get('CLOSED_DATES') or [],
        }

        # Merge raw parsed map so templates can use other keys too
        site.update(parsed)

        return dict(site_settings=site)

    return app
