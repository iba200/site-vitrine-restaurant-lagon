def test_home_page(client):
    """Test that home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Le Lagon" in response.data

def test_menu_page(client):
    """Test that menu page loads."""
    response = client.get('/menu')
    assert response.status_code == 200

def test_contact_page(client):
    """Test that contact page loads."""
    response = client.get('/contact')
    assert response.status_code == 200

def test_reservation_page(client):
    """Test that reservation page loads."""
    response = client.get('/reservation/')
    assert response.status_code == 200

def test_sitemap(client):
    """Test sitemap generation."""
    response = client.get('/sitemap.xml')
    assert response.status_code == 200
    assert b"urlset" in response.data

def test_robots(client):
    """Test robots.txt."""
    response = client.get('/robots.txt')
    assert response.status_code == 200
    assert b"User-agent: *" in response.data
