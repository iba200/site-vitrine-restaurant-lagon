from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, Reservation, MenuItem, Category
from .. import db, limiter
from datetime import date, datetime

admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember_me') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.verify_password(password):
            flash('Email ou mot de passe incorrect.', 'error')
            return redirect(url_for('admin.login'))
            
        login_user(user, remember=remember)
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/login.html')

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@admin.route('/dashboard')
@login_required
def dashboard():
    # Fetch recent reservations
    reservations = Reservation.query.order_by(Reservation.created_at.desc()).limit(10).all()
    today_reservations = Reservation.query.filter(Reservation.date == date.today()).all()
    today_count = len(today_reservations)
    
    # Calculate fill rate (Capacity = 50)
    total_guests_today = sum(r.guests for r in today_reservations if r.status != 'cancelled')
    fill_rate = (total_guests_today / 50) * 100 if total_guests_today > 0 else 0
    
    # Calculate stats for the last 7 days
    from datetime import timedelta
    chart_data = {'labels': [], 'values': []}
    
    for i in range(6, -1, -1):
        day = date.today() - timedelta(days=i)
        count = Reservation.query.filter(Reservation.date == day).count()
        chart_data['labels'].append(day.strftime('%d/%m'))
        chart_data['values'].append(count)
    
    return render_template('admin/dashboard.html', 
                         reservations=reservations, 
                         today_reservations_count=today_count,
                         fill_rate=round(fill_rate, 1),
                         chart_data=chart_data)

# ========== RESERVATIONS MANAGEMENT ==========

@admin.route('/reservations')
@login_required
def reservations():
    status_filter = request.args.get('status')
    search_query = request.args.get('search')
    
    query = Reservation.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
        
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            (Reservation.last_name.ilike(search_term)) | 
            (Reservation.first_name.ilike(search_term))
        )
        
    reservations = query.order_by(Reservation.date.desc(), Reservation.time.desc()).all()
    
    # HTMX request handling for filtration
    if request.headers.get('HX-Request'):
        return render_template('admin/partials/reservations_table_body.html', reservations=reservations)
        
    return render_template('admin/reservations.html', reservations=reservations)

@admin.route('/reservations/<int:id>/status', methods=['POST'])
@login_required
def update_reservation_status(id):
    reservation = Reservation.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'confirmed', 'cancelled', 'completed']:
        reservation.status = new_status
        db.session.commit()
        flash(f'Statut mis à jour : {new_status}', 'success')
    
    # Return updated row for HTMX
    return render_template('admin/partials/reservation_row.html', reservation=reservation)

@admin.route('/reservations/<int:id>/confirm', methods=['POST'])
@login_required
def confirm_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    reservation.status = 'confirmed'
    db.session.commit()
    
    # Send email (mockup logic already in place)
    
    # Return updated row for HTMX
    return render_template('admin/partials/reservation_row.html', reservation=reservation)

@admin.route('/reservations/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin/partials/edit_reservation_modal.html', reservation=reservation)
        
    # POST
    # Note: Complex validation skipped for Admin override power
    reservation.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
    reservation.time = datetime.strptime(request.form.get('time'), '%H:%M').time()
    reservation.guests = int(request.form.get('guests'))
    reservation.status = request.form.get('status')
    reservation.internal_notes = request.form.get('internal_notes')
    
    db.session.commit()
    return render_template('admin/partials/reservation_row.html', reservation=reservation)

@admin.route('/reservations/export')
@login_required
def export_reservations():
    import csv
    import io
    from flask import Response
    
    reservations = Reservation.query.order_by(Reservation.date.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow(['ID', 'Date', 'Heure', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Couverts', 'Statut', 'Créé le'])
    
    for r in reservations:
        writer.writerow([
            r.id, r.date, r.time, r.last_name, r.first_name, 
            r.email, r.phone, r.guests, r.status, r.created_at
        ])
        
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=reservations_export.csv"}
    )

# ========== MENU MANAGEMENT ==========

@admin.route('/menu')
@login_required
def menu():
    current_category = request.args.get('category', 'all')
    categories = Category.query.order_by(Category.order).all()
    
    if current_category == 'all':
        items = MenuItem.query.order_by(MenuItem.order).all()
    else:
        category = Category.query.filter_by(slug=current_category).first()
        items = MenuItem.query.filter_by(category_id=category.id).order_by(MenuItem.order).all() if category else []
    
    return render_template('admin/menu.html', items=items, categories=categories, current_category=current_category)


@admin.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug')
        if not name or not slug:
            flash('Nom et slug requis.', 'error')
            return redirect(url_for('admin.categories'))

        # ensure uniqueness
        existing = Category.query.filter((Category.name == name) | (Category.slug == slug)).first()
        if existing:
            flash('Une catégorie avec ce nom ou slug existe déjà.', 'error')
            return redirect(url_for('admin.categories'))

        cat = Category(name=name, slug=slug)
        db.session.add(cat)
        db.session.commit()
        flash('Catégorie ajoutée.', 'success')
        return redirect(url_for('admin.categories'))

    categories = Category.query.order_by(Category.order).all()
    return render_template('admin/categories.html', categories=categories)


@admin.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    cat = Category.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug')
        if not name or not slug:
            flash('Nom et slug requis.', 'error')
            return redirect(url_for('admin.edit_category', id=id))

        # check uniqueness
        existing = Category.query.filter((Category.slug == slug) | (Category.name == name)).filter(Category.id != id).first()
        if existing:
            flash('Nom ou slug déjà utilisé.', 'error')
            return redirect(url_for('admin.edit_category', id=id))

        cat.name = name
        cat.slug = slug
        db.session.commit()
        flash('Catégorie mise à jour.', 'success')
        return redirect(url_for('admin.categories'))

    return render_template('admin/edit_category.html', category=cat)


@admin.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    cat = Category.query.get_or_404(id)
    # Prevent deletion if category has items
    if cat.items.count() > 0:
        flash('La catégorie contient des plats et ne peut pas être supprimée.', 'error')
        return redirect(url_for('admin.categories'))

    db.session.delete(cat)
    db.session.commit()
    flash('Catégorie supprimée.', 'success')
    return redirect(url_for('admin.categories'))

@admin.route('/menu/add', methods=['POST'])
@login_required
def add_menu_item():
    name = request.form.get('name')
    category_id = int(request.form.get('category_id'))
    description = request.form.get('description')
    price = float(request.form.get('price'))
    
    # Handle Image Upload
    image_url = request.form.get('image_url') # Fallback
    if 'image_file' in request.files:
        file = request.files['image_file']
        if file and file.filename != '':
            from werkzeug.utils import secure_filename
            import os
            from flask import current_app
            
            filename = secure_filename(file.filename)
            # Add timestamp to ensure uniqueness
            import time
            filename = f"{int(time.time())}_{filename}"
            
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            image_url = url_for('static', filename=f'uploads/{filename}')

    item = MenuItem(
        name=name,
        category_id=category_id,
        description=description,
        price=price,
        image_url=image_url,
        is_special=request.form.get('is_special') == 'true',
        is_available=request.form.get('is_available') == 'true'
    )
    
    db.session.add(item)
    db.session.commit()

    html = render_template('admin/partials/menu_item_card.html', item=item)
    from flask import make_response
    response = make_response(html)
    # Trigger a client-side HTMX event so public menu can refresh
    response.headers['HX-Trigger'] = 'menuUpdated'
    return response

@admin.route('/menu/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_menu_item(id):
    item = MenuItem.query.get_or_404(id)
    
    if request.method == 'GET':
        categories = Category.query.order_by(Category.order).all()
        return render_template('admin/partials/edit_menu_item_modal.html', item=item, categories=categories)
    
    # POST - Update item
    item.name = request.form.get('name')
    item.category_id = int(request.form.get('category_id'))
    item.description = request.form.get('description')
    item.price = float(request.form.get('price'))
    
    # Handle Image Update
    if 'image_file' in request.files:
        file = request.files['image_file']
        if file and file.filename != '':
            from werkzeug.utils import secure_filename
            import os
            from flask import current_app
            import time
            
            filename = secure_filename(file.filename)
            filename = f"{int(time.time())}_{filename}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            item.image_url = url_for('static', filename=f'uploads/{filename}')
    elif request.form.get('image_url'):
         item.image_url = request.form.get('image_url')

    item.is_special = request.form.get('is_special') == 'true'
    item.is_available = request.form.get('is_available') == 'true'
    
    db.session.commit()
    html = render_template('admin/partials/menu_item_card.html', item=item)
    from flask import make_response
    response = make_response(html)
    response.headers['HX-Trigger'] = 'menuUpdated'
    return response

@admin.route('/menu/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_menu_item(id):
    item = MenuItem.query.get_or_404(id)
    item.is_available = not item.is_available
    db.session.commit()
    
    return render_template('admin/partials/menu_item_card.html', item=item)

@admin.route('/menu/reorder', methods=['POST'])
@login_required
def reorder_menu():
    """
    Expects JSON data: { "items": ["1", "3", "2"] } where strings are item IDs in new order.
    """
    data = request.get_json()
    if not data or 'items' not in data:
        return {'status': 'error'}, 400
        
    for index, item_id in enumerate(data['items']):
        item = MenuItem.query.get(int(item_id))
        if item:
            item.order = index
            
    db.session.commit()
    return {'status': 'success'}

@admin.route('/menu/<int:id>', methods=['DELETE'])
@login_required
def delete_menu_item(id):
    item = MenuItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    # Also support HTMX triggers for public menu refresh
    from flask import make_response
    response = make_response('', 200)
    response.headers['HX-Trigger'] = 'menuUpdated'
    return response


@admin.route('/menu/<int:id>/delete', methods=['POST'])
@login_required
def delete_menu_post(id):
    # POST-based delete endpoint to avoid CSRF issues with DELETE in some clients
    item = MenuItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    from flask import make_response
    response = make_response('', 200)
    response.headers['HX-Trigger'] = 'menuUpdated'
    return response
