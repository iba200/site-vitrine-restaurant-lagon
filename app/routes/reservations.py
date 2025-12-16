from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
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

        # Create reservation object
        reservation = Reservation(
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            time=datetime.strptime(time_str, '%H:%M').time(),
            guests=int(guests),
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
