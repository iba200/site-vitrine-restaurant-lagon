from flask import Blueprint, render_template, Response, url_for, current_app, redirect, request, flash
from .. import mail, db
from flask_mail import Message as MailMessage
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/menu')
def menu():
    return render_template('menu.html')

@main.route('/reservation') # Explicit alias if needed, primarily handled by blueprint but good for sitemap
def reservation_redirect():
    return redirect(url_for('reservations.index'))

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Basic contact form handling: validate, persist, and optionally send email
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        message = (request.form.get('message') or '').strip()

        # Simple validation
        errors = []
        if not name:
            errors.append('Le nom est requis.')
        if not email or '@' not in email:
            errors.append('Un email valide est requis.')
        if not message or len(message) < 10:
            errors.append('Le message est trop court (au moins 10 caractères).')

        if errors:
            for e in errors:
                flash(e, 'error')
            return redirect(url_for('main.contact'))

        # Persist message
        try:
            from ..models import Settings, ContactMessage
            cm = ContactMessage(name=name, email=email, message=message, ip=request.remote_addr)
            db.session.add(cm)
            db.session.commit()
        except Exception:
            # If DB fails, continue but log via flash
            flash('Impossible d\'enregistrer le message sur le serveur, mais le message sera tenté d\'être envoyé.', 'error')

        # Compose notification recipients
        recipients = []
        try:
            notif = Settings.get('NOTIFICATION_EMAILS', default=None, as_json=True) or []
            if isinstance(notif, list) and notif:
                recipients = notif
        except Exception:
            recipients = []

        # Fallback to contact email
        if not recipients:
            recipients = [current_app.config.get('MAIL_DEFAULT_RECEIVER') or Settings.get('CONTACT_EMAIL', default=None) or current_app.config.get('CONTACT_EMAIL')]

        # Send email if mail is configured and recipients available
        try:
            if mail and recipients and recipients[0]:
                msg = MailMessage(subject=f"Contact form: {name or 'Sans nom'}",
                              sender=email or current_app.config.get('MAIL_DEFAULT_SENDER'),
                              recipients=[r for r in recipients if r])
                body = f"Nom: {name}\nEmail: {email}\n\nMessage:\n{message}"
                msg.body = body
                mail.send(msg)
        except Exception:
            # Don't fail on email errors; continue
            pass

        flash('Votre message a bien été envoyé. Nous vous répondrons dès que possible.', 'success')
        return redirect(url_for('main.contact'))

    return render_template('contact.html')

@main.route('/mentions-legales')
def mentions_legales():
    return render_template('mentions_legales.html')

@main.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml dynamically."""
    pages = []
    
    # Static pages
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            if not rule.rule.startswith('/admin') and not rule.rule.startswith('/api'):
                 pages.append(
                     [url_for(rule.endpoint, _external=True), datetime.now().date().isoformat()]
                 )
    
    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    return Response(sitemap_xml, mimetype='application/xml')

@main.route('/robots.txt')
def robots():
    """Generate robots.txt."""
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /api/",
        f"Sitemap: {url_for('main.sitemap', _external=True)}"
    ]
    return Response("\n".join(lines), mimetype='text/plain')
