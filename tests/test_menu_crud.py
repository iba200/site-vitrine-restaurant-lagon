import io
from app.models import User, Category, MenuItem
from app import db


def test_menu_crud_flow(app, client):
    # Setup user and category
    with app.app_context():
        user = User(username='admin', email='admin@example.com')
        user.password = 'secret'
        db.session.add(user)
        cat = Category(name='Test', slug='test')
        db.session.add(cat)
        db.session.commit()

    # Login
    resp = client.post('/admin/login', data={'email': 'admin@example.com', 'password': 'secret'}, follow_redirects=True)
    assert resp.status_code in (200, 302)

    # Add menu item with file upload
    data = {
        'name': 'Test Dish',
        'category_id': str(cat.id),
        'description': 'A test dish',
        'price': '12.50',
        'is_available': 'true'
    }
    file_data = (io.BytesIO(b'testimagecontent'), 'test.png')
    data['image_file'] = file_data

    resp = client.post('/admin/menu/add', data=data, content_type='multipart/form-data')
    assert resp.status_code == 200

    with app.app_context():
        item = MenuItem.query.filter_by(name='Test Dish').first()
        assert item is not None
        item_id = item.id

    # Toggle availability
    resp = client.post(f'/admin/menu/{item_id}/toggle')
    assert resp.status_code == 200

    # Delete item
    resp = client.post(f'/admin/menu/{item_id}/delete')
    assert resp.status_code == 200

    with app.app_context():
        assert MenuItem.query.get(item_id) is None
