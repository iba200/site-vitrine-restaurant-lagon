from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from ..models import MenuItem, Category, Reservation
from flask import current_app

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

    # Determine requested guests
    if not guests:
        requested = 1
    elif guests == 'more':
        return render_template('components/slots.html', slots={}, error="Pour plus de 12 personnes, contactez-nous")
    else:
        try:
            requested = int(guests)
        except ValueError:
            requested = 1

    capacity = int(current_app.config.get('CAPACITY', 50))
    table_duration = timedelta(hours=2)

    # Fetch existing reservations for the date
    existing = Reservation.query.filter(Reservation.date == selected_date, Reservation.status != 'cancelled').all()

    def slot_is_available(slot_time_str):
        slot_time = datetime.strptime(slot_time_str, '%H:%M').time()
        slot_start = datetime.combine(selected_date, slot_time)
        slot_end = slot_start + table_duration

        overlapping = 0
        for r in existing:
            try:
                r_start = datetime.combine(r.date, r.time)
            except Exception:
                continue
            r_end = r_start + table_duration
            if not (r_end <= slot_start or r_start >= slot_end):
                overlapping += (r.guests or 0)

        return (capacity - overlapping) >= requested

    # Generate lunch slots (12:00 to 14:00)
    lunch_slots = []
    current_slot = datetime.strptime('12:00', '%H:%M')
    end_slot = datetime.strptime('14:00', '%H:%M')
    while current_slot <= end_slot:
        s = current_slot.strftime('%H:%M')
        if slot_is_available(s):
            lunch_slots.append(s)
        current_slot += timedelta(minutes=30)

    # Generate dinner slots (19:00 to 22:00)
    dinner_slots = []
    current_slot = datetime.strptime('19:00', '%H:%M')
    end_slot = datetime.strptime('22:00', '%H:%M')
    while current_slot <= end_slot:
        s = current_slot.strftime('%H:%M')
        if slot_is_available(s):
            dinner_slots.append(s)
        current_slot += timedelta(minutes=30)

    return render_template('components/slots.html', slots={'lunch': lunch_slots, 'dinner': dinner_slots})
