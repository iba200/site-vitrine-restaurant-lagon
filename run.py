import os
from app import create_app, db
from app.models import User, Reservation, MenuItem, Category, Settings

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Reservation=Reservation, MenuItem=MenuItem, Category=Category, Settings=Settings)

if __name__ == '__main__':
    app.run()
