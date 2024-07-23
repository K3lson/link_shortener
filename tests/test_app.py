import pytest
from app import create_app,db
from app.models import URL


@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield appdb.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'URL Shortener' in response.data


def test_url_shortening(client):
    response = client.post('/', data={'original_url': 'https://www.example.com'})
    assert response.status_code == 200
    assert URL.query.count() == 1
    url = URL.query.first()
    assert url.original_url == 'https://www.example.com'
    assert len(url.short_url) == 6

def test_url_redirection(client):
    url = URL(original_url='https://www.example.com')
    db.session.add(url)
    db.session.commit()

    response = client.get(f'/{url.short_url}')
    assert response.status_code == 302
    assert response.location == 'https://www.example.com'