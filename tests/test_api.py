import pytest
from app import create_app, db
from app.models import Item


@pytest.fixture
def app():
    """Create and configure a test app."""
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    }
    flask_app = create_app(config=test_config)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's CLI."""
    return app.test_cli_runner()

# ── Search Items Tests ──────────────────────────────────────
def test_search_items(client, app):
    """Test searching items by name."""
    with app.app_context():
        item1 = Item(name='Apple pie', description='A delicious pie')
        item2 = Item(name='Banana bread', description='A tasty bread')
        item3 = Item(name='Apple juice', description='A fresh juice')
        db.session.add_all([item1, item2, item3])
        db.session.commit()

    response = client.get('/api/items/search?name=Apple')
    assert response.status_code == 200
    results = response.json
    assert len(results) == 2
    assert all('Apple' in item['name'] for item in results)


def test_search_items_missing_param(client):
    """Test search without name parameter returns 400."""
    response = client.get('/api/items/search')
    assert response.status_code == 400
    assert 'required' in response.json['error'].lower()

# ── Health Check Tests ──────────────────────────────────────
def test_health(client):
    """Test health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'


# ── Get All Items Tests ──────────────────────────────────────
def test_get_all_items_empty(client):
    """Test retrieving items when database is empty."""
    response = client.get('/api/items')
    assert response.status_code == 200
    assert response.json == []


def test_get_all_items(client, app):
    """Test retrieving all items."""
    with app.app_context():
        item1 = Item(name='Item 1', description='First item')
        item2 = Item(name='Item 2', description='Second item')
        db.session.add_all([item1, item2])
        db.session.commit()
    
    response = client.get('/api/items')
    assert response.status_code == 200
    items = response.json
    assert len(items) == 2
    assert items[0]['name'] == 'Item 1'
    assert items[1]['name'] == 'Item 2'


# ── Create Item Tests ──────────────────────────────────────
def test_create_item(client):
    """Test creating a new item."""
    response = client.post('/api/items', json={
        'name': 'Test Item',
        'description': 'A test item'
    })
    assert response.status_code == 201
    data = response.json
    assert data['item']['name'] == 'Test Item'
    assert data['item']['description'] == 'A test item'
    assert 'id' in data['item']


def test_create_item_without_description(client):
    """Test creating an item without description."""
    response = client.post('/api/items', json={'name': 'Simple Item'})
    assert response.status_code == 201
    assert response.json['item']['name'] == 'Simple Item'
    assert response.json['item']['description'] is None


def test_create_item_missing_name(client):
    """Test creating an item without name fails."""
    response = client.post('/api/items', json={'description': 'No name'})
    assert response.status_code == 400
    assert 'required' in response.json['error'].lower()


# ── Get Single Item Tests ──────────────────────────────────────
def test_get_item(client, app):
    """Test retrieving a single item by ID."""
    with app.app_context():
        item = Item(name='Single Item', description='Test')
        db.session.add(item)
        db.session.commit()
        item_id = item.id
    
    response = client.get(f'/api/items/{item_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Single Item'


def test_get_item_not_found(client):
    """Test retrieving non-existent item."""
    response = client.get('/api/items/999')
    assert response.status_code == 404


# ── Update Item Tests ──────────────────────────────────────
def test_update_item(client, app):
    """Test updating an item."""
    with app.app_context():
        item = Item(name='Original', description='Original desc')
        db.session.add(item)
        db.session.commit()
        item_id = item.id
    
    response = client.put(f'/api/items/{item_id}', json={
        'name': 'Updated',
        'description': 'Updated desc'
    })
    assert response.status_code == 200
    assert response.json['item']['name'] == 'Updated'
    assert response.json['item']['description'] == 'Updated desc'


# ── Delete Item Tests ──────────────────────────────────────
def test_delete_item(client, app):
    """Test deleting an item."""
    with app.app_context():
        item = Item(name='To Delete', description='Will be deleted')
        db.session.add(item)
        db.session.commit()
        item_id = item.id
    
    response = client.delete(f'/api/items/{item_id}')
    assert response.status_code == 200
    assert 'deleted' in response.json['message'].lower()
    
    # Verify item is gone
    response = client.get(f'/api/items/{item_id}')
    assert response.status_code == 404


# ── Root Endpoint Tests ──────────────────────────────────────
def test_root_endpoint(client):
    """Test root API endpoint."""
    response = client.get('/api/')
    assert response.status_code == 200
    data = response.json
    assert data['name'] == 'Flask MySQL API'
    assert 'endpoints' in data
