from flask import Blueprint, render_template, Response, url_for, current_app, redirect
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

@main.route('/contact')
def contact():
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
