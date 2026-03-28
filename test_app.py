import pytest
import json
from app import app, inventory_db, InventoryItem

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            inventory_db.clear()
            yield client

@pytest.fixture
def sample_item():
    return InventoryItem(name="Test Product")

def post_item(client, data):
    return client.post('/inventory',
                       data=json.dumps(data),
                       content_type='application/json')

def patch_item(client, item_id, data):
    return client.patch(f'/inventory/{item_id}',
                        data=json.dumps(data),
                        content_type='application/json')

class TestInventoryRoutes:

    def test_get_empty_inventory(self, client):
        response = client.get('/inventory')
        assert response.status_code == 200
        assert response.json == []

    def test_adding_item_works(self, client):
        data = {'name': 'Test Product', 'quantity': 10, 'price': 5.99}
        response = post_item(client, data)
        assert response.status_code == 201
        result = response.json
        assert result['name'] == 'Test Product'
        assert result['quantity'] == 10
        assert result['price'] == 5.99
        assert 'id' in result
        assert 'created_at' in result

    def test_add_item_no_name(self, client):
        data = {'quantity': 10, 'price': 5.99}
        response = post_item(client, data)
        assert response.status_code == 400
        assert 'error' in response.json

    def test_add_item_only_name(self, client):
        response = post_item(client, {'name': 'Simple Product'})
        assert response.status_code == 201
        result = response.json
        assert result['name'] == 'Simple Product'

    def test_get_single_item(self, client, sample_item):
        inventory_db.append(sample_item)
        response = client.get(f'/inventory/{sample_item.id}')
        assert response.status_code == 200
        result = response.json
        assert result['id'] == sample_item.id
        assert result['name'] == sample_item.name

    def test_item_doesnt_exist(self, client):
        response = client.get('/inventory/non-existent-id')
        assert response.status_code == 404
        assert 'error' in response.json

    def test_update_works(self, client, sample_item):
        inventory_db.append(sample_item)
        update_data = {'name': 'Updated Product', 'quantity': 20, 'price': 7.99}
        response = patch_item(client, sample_item.id, update_data)
        assert response.status_code == 200
        result = response.json
        assert result['name'] == 'Updated Product'
        assert result['quantity'] == 20
        assert result['price'] == 7.99
        assert result['updated_at'] != sample_item.updated_at

    def test_partial_update(self, client, sample_item):
        inventory_db.append(sample_item)
        response = patch_item(client, sample_item.id, {'price': 9.99})
        assert response.status_code == 200
        result = response.json
        assert result['name'] == sample_item.name
        assert result['price'] == 9.99
        assert result['quantity'] == sample_item.quantity

    def test_update_missing_item(self, client):
        response = patch_item(client, 'non-existent-id', {'name': 'Updated Product'})
        assert response.status_code == 404
        assert 'error' in response.json

    def test_delete_works(self, client, sample_item):
        inventory_db.append(sample_item)
        item_id = sample_item.id
        response = client.delete(f'/inventory/{item_id}')
        assert response.status_code == 200
        result = response.json
        assert 'message' in result
        assert 'deleted_item' in result
        assert result['deleted_item']['id'] == item_id
        assert len(inventory_db) == 0

    def test_delete_missing_item(self, client):
        response = client.delete('/inventory/non-existent-id')
        assert response.status_code == 404
        assert 'error' in response.json

    def test_search_by_name_found_in_inventory(self, client, sample_item):
        inventory_db.append(sample_item)
        response = client.get(f'/inventory/search/name/Test')
        assert response.status_code == 200
        result = response.json
        assert result[0]['id'] == sample_item.id

    def test_search_by_name_found(self, client, sample_item):
        inventory_db.append(sample_item)
        response = client.get('/inventory/search/name/Test')
        assert response.status_code == 200
        results = response.json
        assert len(results) == 1
        assert results[0]['id'] == sample_item.id

    def test_search_by_name_case_insensitive(self, client, sample_item):
        inventory_db.append(sample_item)
        response = client.get('/inventory/search/name/test')
        assert response.status_code == 200
        results = response.json
        assert len(results) == 1
        assert results[0]['id'] == sample_item.id

    def test_search_by_name_not_found(self, client):
        response = client.get('/inventory/search/name/NonExistent')
        assert response.status_code == 200
        assert response.json == []


class TestInventoryModel:

    def test_inventory_item_creation(self):
        item = InventoryItem(name="Test Product")
        assert item.name == "Test Product"
        assert item.id is not None
        assert item.created_at is not None
        assert item.updated_at is not None
        assert item.product_details == {}

    def test_inventory_item_to_dict(self):
        item = InventoryItem(name="Test Product")
        item_dict = item.to_dict()
        assert isinstance(item_dict, dict)
        assert item_dict['name'] == "Test Product"
        assert 'id' in item_dict
        assert 'created_at' in item_dict
        assert 'updated_at' in item_dict
        assert 'product_details' in item_dict

    def test_inventory_item_minimal_creation(self):
        item = InventoryItem(name="Simple Product")
        assert item.name == "Simple Product"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
