import json
from app.app import app, convert_amount, SUPPORTED_CURRENCIES, RATES


def test_convert_amount():
    assert convert_amount(100, "USD", "EUR") == 92
    assert convert_amount(100, "EUR", "USD") == 108.6957
    assert convert_amount(100, "USD", "GBP") == 78
    assert convert_amount(100, "USD", "JPY") == 15500


def test_supported_currencies():
    assert sorted(SUPPORTED_CURRENCIES) == ["EUR", "GBP", "JPY", "USD"]
    assert set(RATES.keys()) == SUPPORTED_CURRENCIES


def test_health_endpoint():
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {'status': 'ok'}


def test_convert_endpoint():
    with app.test_client() as client:
        # Valid conversion
        response = client.post('/convert', json={
            'amount': 100,
            'from': 'USD',
            'to': 'EUR'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'converted' in data
        assert data['converted'] == 92

        # Invalid currency
        response = client.post('/convert', json={
            'amount': 100,
            'from': 'XYZ',
            'to': 'EUR'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'].startswith('unsupported')

        # Missing amount
        response = client.post('/convert', json={
            'from': 'USD',
            'to': 'EUR'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data == {'error': '`amount` is required'}
