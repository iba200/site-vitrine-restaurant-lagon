from . import scheduler, db, mail
from .models import Reservation
from flask_mail import Message
from datetime import datetime, timedelta
from flask import current_app

def send_reminders():
    """Send reminders for reservations tomorrow."""
    with scheduler.app.app_context():
        tomorrow = datetime.now().date() + timedelta(days=1)
        reservations = Reservation.query.filter_by(date=tomorrow, status='confirmed').all()
        
        for reservation in reservations:
            try:
                msg = Message(
                    subject=f'Rappel: Votre réservation demain - Le Lagon',
                    sender=current_app.config['MAIL_USERNAME'] or ('Le Lagon', 'noreply@lelagon.com'),
                    recipients=[reservation.email]
                )
                msg.body = f"""Bonjour {reservation.first_name},

Ceci est un rappel pour votre réservation demain à {reservation.time.strftime('%H:%M')} pour {reservation.guests} personnes.

Si vous avez un empêchement, merci de nous contacter.

À demain !
L'équipe Le Lagon
"""
                mail.send(msg)
                print(f"Reminder sent to {reservation.email}")
            except Exception as e:
                print(f"Failed to send reminder to {reservation.email}: {e}")
