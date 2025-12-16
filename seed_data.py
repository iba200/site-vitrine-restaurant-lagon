from app import create_app, db
from app.models import User, Category, MenuItem
import os

app = create_app('default')

with app.app_context():
    # Create Admin User
    if not User.query.filter_by(email='admin@lelagon.com').first():
        admin = User(username='admin', email='admin@lelagon.com')
        admin.password = 'ChangeMeNow123!'
        db.session.add(admin)
        print("Admin user created.")

    # Create Categories
    categories_data = [
        {'name': 'Entrées', 'slug': 'entrees', 'order': 1},
        {'name': 'Plats', 'slug': 'plats', 'order': 2},
        {'name': 'Desserts', 'slug': 'desserts', 'order': 3},
        {'name': 'Boissons', 'slug': 'boissons', 'order': 4},
    ]
    
    for cat_data in categories_data:
        if not Category.query.filter_by(slug=cat_data['slug']).first():
            category = Category(**cat_data)
            db.session.add(category)
    db.session.commit()
    print("Categories created.")

    # Create Menu Items
    # Need to query categories first to get IDs
    entrees = Category.query.filter_by(slug='entrees').first()
    plats = Category.query.filter_by(slug='plats').first()
    desserts = Category.query.filter_by(slug='desserts').first()

    items_data = [
        {
            'name': 'Accras de Morue',
            'category': entrees,
            'description': 'Beignets de morue croustillants, sauce chien maison.',
            'price': 12.00,
            'image_url': 'https://images.unsplash.com/photo-1544510803-91b5d1e2e75e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_special': False,
            'dietary_tags': ''
        },
        {
            'name': 'Ceviche de Daurade',
            'category': entrees,
            'description': 'Daurade fraîche marinée au citron vert, lait de coco et piment doux.',
            'price': 16.00,
            'image_url': 'https://images.unsplash.com/photo-1548590393-271d49c6cb4f?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_special': True,
            'dietary_tags': 'gluten-free'
        },
        {
            'name': 'Langouste Grillée',
            'category': plats,
            'description': 'Langouste entière grillée au beurre d\'ail, riz créole.',
            'price': 45.00,
            'image_url': 'https://images.unsplash.com/photo-1553163147-62199b433433?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_special': True,
            'dietary_tags': 'gluten-free'
        },
        {
            'name': 'Colombo de Poulet',
            'category': plats,
            'description': 'Poulet mijoté aux épices colombo, légumes pays.',
            'price': 18.00,
            'image_url': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_special': False,
            'dietary_tags': ''
        },
        {
            'name': 'Veggie Curry',
            'category': plats,
            'description': 'Légumes de saison au lait de coco et curry doux, quinoa.',
            'price': 16.00,
            'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_special': False,
            'dietary_tags': 'vegetarian,vegan'
        },
        {
            'name': 'Blanc Manger Coco',
            'category': desserts,
            'description': 'Flan traditionnel au lait de coco, coulis de fruits rouges.',
            'price': 8.00,
            'image_url': 'https://plus.unsplash.com/premium_photo-1695028377749-0d19c1ccf464?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_special': False,
            'dietary_tags': 'vegetarian'
        }
    ]

    for item in items_data:
        if not MenuItem.query.filter_by(name=item['name']).first():
            menu_item = MenuItem(
                name=item['name'],
                category_id=item['category'].id,
                description=item['description'],
                price=item['price'],
                image_url=item['image_url'],
                is_special=item['is_special'],
                dietary_tags=item['dietary_tags']
            )
            db.session.add(menu_item)
    
    db.session.commit()
    print("Menu items created.")

print("Seeding complete.")
