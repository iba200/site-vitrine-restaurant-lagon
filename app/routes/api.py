from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from ..models import MenuItem, Category

api = Blueprint('api', __name__)

@api.route('/menu/filter')
def filter_menu():
    category_slug = request.args.get('category', 'all')
    search_query = request.args.get('q', '').lower()
    is_vegetarian = request.args.get('vegetarian') == 'true'
    
    query = MenuItem.query.filter_by(is_available=True)
    
    # Filter by category
    if category_slug != 'all':
        query = query.join(Category).filter(Category.slug == category_slug)
    
    # Filter by search query
    if search_query:
        query = query.filter(MenuItem.name.ilike(f'%{search_query}%'))
    
    # Filter by vegetarian
    if is_vegetarian:
        query = query.filter(MenuItem.dietary_tags.ilike('%vegetarian%'))
    
    items = query.order_by(MenuItem.order).all()
    
    return render_template('components/menu_items.html', items=items)

@api.route('/check-availability', methods=['POST'])
def check_availability():
    date_str = request.form.get('date')
    guests = request.form.get('guests')
    
    if not date_str:
        return render_template('components/slots.html', slots={}, error="Veuillez sélectionner une date")

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return render_template('components/slots.html', slots={}, error="Format de date invalide")

    # Check if Monday (0=Monday in Python date.weekday())
    if selected_date.weekday() == 0:
        return render_template('components/slots.html', slots={}, error="Le restaurant est fermé le lundi")

    # Mock availability logic
    # In a real app, we would query the Reservations table here
    # to count existing guests per slot
    
    lunch_slots = []
    dinner_slots = []
    
    # Generate lunch slots (12:00 to 14:00)
    current_time = datetime.strptime('12:00', '%H:%M')
    end_time = datetime.strptime('14:00', '%H:%M')
    while current_time <= end_time:
        lunch_slots.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=30)

    # Generate dinner slots (19:00 to 22:00)
    current_time = datetime.strptime('19:00', '%H:%M')
    end_time = datetime.strptime('22:00', '%H:%M')
    while current_time <= end_time:
        dinner_slots.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=30)

    return render_template('components/slots.html', slots={'lunch': lunch_slots, 'dinner': dinner_slots})
