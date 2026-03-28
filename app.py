from flask import Flask, request, jsonify
import requests
import uuid
from datetime import datetime, timezone

app = Flask(__name__)

# Mock database to store inventory items
inventory_db = []

class InventoryItem:
    def __init__(self, name, barcode=None, quantity=0, price=0.0):
        self.id = str(uuid.uuid4())
        self.name = name
        self.barcode = barcode
        self.quantity = quantity
        self.price = price
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = datetime.now(timezone.utc).isoformat()
        self.product_details = {}

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'barcode': self.barcode,
            'quantity': self.quantity,
            'price': self.price,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'product_details': self.product_details
        }

def fetch_product_from_openfoodfacts(barcode):
    """Fetch product details from OpenFoodFacts API"""
    if not barcode or not str(barcode).isdigit():
        return None
    try:
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        headers = {
            'User-Agent': 'InventoryManager/1.0 (test@example.com)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 1:
                product = data.get('product', {})
                return {
                    'product_name': product.get('product_name', ''),
                    'brands': product.get('brands', ''),
                    'ingredients_text': product.get('ingredients_text', ''),
                    'categories': product.get('categories', ''),
                    'nutriscore_grade': product.get('nutriscore_grade', ''),
                    'nova_group': product.get('nova_group', ''),
                    'ecoscore_grade': product.get('ecoscore_grade', '')
                }
        return None
    except Exception as e:
        print(f"Error fetching product: {e}")
        return None

# CRUD Routes
@app.route('/inventory', methods=['GET'])
def get_all_inventory():
    """Get all inventory items"""
    return jsonify([item.to_dict() for item in inventory_db])

@app.route('/inventory/<item_id>', methods=['GET'])
def get_inventory_item(item_id):
    """Get a single inventory item by ID"""
    for item in inventory_db:
        if item.id == item_id:
            return jsonify(item.to_dict())
    return jsonify({'error': 'Item not found'}), 404

@app.route('/inventory', methods=['POST'])
def add_inventory_item():
    """Add a new inventory item"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    # Create new inventory item
    item = InventoryItem(
        name=data['name'],
        barcode=data.get('barcode'),
        quantity=data.get('quantity', 0),
        price=data.get('price', 0.0)
    )
    
    inventory_db.append(item)
    return jsonify(item.to_dict()), 201

@app.route('/inventory/<item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    item_to_delete = None
    index = None
    for i, item in enumerate(inventory_db):
        if item.id == item_id:
            item_to_delete = item
            index = i
            break
    if item_to_delete is None:
        return jsonify({'error': 'Item not found'}), 404
    inventory_db.pop(index)
    return jsonify({'message': 'Item deleted successfully', 'deleted_item': item_to_delete.to_dict()})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)