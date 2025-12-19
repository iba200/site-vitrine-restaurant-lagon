from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime, timedelta
from .. import db, limiter
from ..models import Reservation

reservations = Blueprint('reservations', __name__)

@reservations.route('/', methods=['GET'])
def index():
    return render_template('reservation.html')

@reservations.route('/confirm', methods=['POST'])
@limiter.limit("10 per hour")
def confirm():
    try:
        # Extract form data
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        guests = request.form.get('guests')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        special_requests = request.form.get('special_requests')

        if not all([date_str, time_str, guests, first_name, last_name, email, phone]):
            flash('Veuillez remplir tous les champs obligatoires.', 'error')
            return redirect(url_for('reservations.index'))
        # Parse date/time
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            time_obj = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            flash('Format de date/heure invalide.', 'error')
            return redirect(url_for('reservations.index'))

        # Guests handling
        if guests == 'more':
            flash('Pour plus de 12 personnes, merci de contacter le restaurant directement.', 'error')
            return redirect(url_for('reservations.index'))

        try:
            guests_int = int(guests)
        except ValueError:
            flash('Nombre de personnes invalide.', 'error')
            return redirect(url_for('reservations.index'))

        # Business rules
        capacity = int(current_app.config.get('CAPACITY', 50))
        table_duration = timedelta(hours=2)

        new_start = datetime.combine(date_obj, time_obj)
        new_end = new_start + table_duration
        now = datetime.now()

        # No reservations less than 2 hours from now
        if new_start - now < timedelta(hours=2):
            flash('Les réservations doivent être effectuées au moins 2 heures à l\'avance.', 'error')
            return redirect(url_for('reservations.index'))

        # No reservations more than 60 days in advance
        if date_obj > (now.date() + timedelta(days=60)):
            flash('Les réservations ne peuvent pas être faites plus de 2 mois à l\'avance.', 'error')
            return redirect(url_for('reservations.index'))

        # Check capacity for overlapping reservations on the same date
        overlapping_guests = 0
        existing = Reservation.query.filter(Reservation.date == date_obj, Reservation.status != 'cancelled').all()
        for r in existing:
            try:
                exist_start = datetime.combine(r.date, r.time)
            except Exception:
                continue
            exist_end = exist_start + table_duration
            # intervals overlap?
            if not (exist_end <= new_start or exist_start >= new_end):
                overlapping_guests += (r.guests or 0)

        if overlapping_guests + guests_int > capacity:
            flash('Désolé, il n\'y a plus de places disponibles pour ce créneau.', 'error')
            return redirect(url_for('reservations.index'))

        # Create reservation object
        reservation = Reservation(
            date=date_obj,
            time=time_obj,
            guests=guests_int,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            special_requests=special_requests,
            status='confirmed' # Auto-confirm for MVP
        )

        db.session.add(reservation)
        db.session.commit()

        # Send confirmation email
        try:
            from flask_mail import Message
            from .. import mail
            
            msg = Message(
                subject=f'Confirmation de réservation - Le Lagon - {date_str}',
                sender=current_app.config['MAIL_USERNAME'] or ('Le Lagon', 'noreply@lelagon.com'),
                recipients=[email]
            )
            msg.body = f"""Bonjour {first_name} {last_name},

Votre réservation au restaurant Le Lagon est confirmée.

Détails de la réservation :
- Date : {date_str}
- Heure : {time_str}
- Nombre de personnes : {guests}
- Téléphone : {phone}

Nous avons hâte de vous accueillir !

Cordialement,
L'équipe Le Lagon
"""
            mail.send(msg)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Error sending email: {e}")

        flash('Votre réservation a été confirmée avec succès ! Un email vous sera envoyé.', 'success')
        return redirect(url_for('main.index'))

    except Exception as e:
        db.session.rollback()
        flash(f'Une erreur est survenue : {str(e)}', 'error')
        return redirect(url_for('reservations.index'))
