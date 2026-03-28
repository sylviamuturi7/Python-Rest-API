#!/usr/bin/env python3
"""
Demo script to showcase the inventory management system
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)

def print_response(response, title="Response"):
    print(f"\n{title}:")
    print(f"Status Code: {response.status_code}")
    if response.headers.get('content-type', '').startswith('application/json'):
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.text)

def add_demo_item(item_data):
    response = requests.post(f"{BASE_URL}/inventory", json=item_data)
    print_response(response, "Added Item")
    return response

def get_all_items():
    print("\n2. Getting all inventory items...")
    response = requests.get(f"{BASE_URL}/inventory")
    print_response(response, "All Items")

def get_item(item_id):
    print("\n3. Getting specific item by ID...")
    # Validate item_id 
    if not isinstance(item_id, str) or not item_id.replace('-', '').replace('_', '').isalnum():
        print("Invalid item_id format")
        return
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    print_response(response, "Specific Item")

def update_item(item_id, update_data):
    print("\n4. Updating item quantity and price...")
    # Validate item_id 
    if not isinstance(item_id, str) or not item_id.replace('-', '').replace('_', '').isalnum():
        print("Invalid item_id format")
        return
    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=update_data)
    print_response(response, "Updated Item")

def delete_item(item_id):
    print("\n5. Deleting item...")
    # Validate item_id 
    if not isinstance(item_id, str) or not item_id.replace('-', '').replace('_', '').isalnum():
        print("Invalid item_id format")
        return
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    print_response(response, "Deleted Item")

def verify_deletion(item_id):
    print("6. Verifying item was deleted...")
    # Validate item_id 
    if not isinstance(item_id, str) or not item_id.replace('-', '').replace('_', '').isalnum():
        print("Invalid item_id format")
        return
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    print_response(response, "Verify Deletion")

def demo_basic_operations():
    print_section("DEMO: Basic CRUD Operations")
    print("\n1. Adding a new inventory item...")
    item_data = {
        'name': 'Organic Oat Milk',
        'quantity': 25,
        'price': 40.99
    }
    response = add_demo_item(item_data)
    if response.status_code == 201:
        item_id = response.json()['id']
        get_all_items()
        get_item(item_id)
        update_item(item_id, {'quantity': 30, 'price': 50.49})
        delete_item(item_id)
        verify_deletion(item_id)

def add_search_test_items():
    test_items = [
        {'name': 'Apple iPhone 17', 'quantity': 10, 'price': 70000.99},
        {'name': 'Samsung Galaxy S26', 'quantity': 8, 'price': 7899.99},
        {'name': 'Apple MacBook Pro', 'quantity': 5, 'price': 215999.99}
    ]
    print("\nAdding test items for search demo...")
    for item in test_items:
        requests.post(f"{BASE_URL}/inventory", json=item)

def demo_search_functionality():
    print_section("DEMO: Search Functionality")
    add_search_test_items()
    print("\n1. Searching by name 'Apple'...")
    response = requests.get(f"{BASE_URL}/inventory/search/name/Apple")
    print_response(response, "Search by Name")

def demo_openfoodfacts_integration():
    print_section("DEMO: OpenFoodFacts Integration")
    print("\n1. Adding item with real Coca-Cola...")
    item_data = {
        'name': 'Coca-Cola No Sugar',
        'quantity': 50,
        'price': 1.99
    }
    response = add_demo_item(item_data)
    if response.status_code == 201:
        item_id = response.json()['id']
        print("\n2. Getting item details...")
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        print_response(response, "Item with Product Details")

FAKE_ID = "non-existent-id"

def demo_error_handling():
    print_section("DEMO: Error Handling")
    print("\n1. Trying to add item without name...")
    response = requests.post(f"{BASE_URL}/inventory", json={
        'quantity': 10,
        'price': 50.99
    })
    print_response(response, "Missing Name Error")
    print("\n2. Trying to get non-existent item...")
    response = requests.get(f"{BASE_URL}/inventory/{FAKE_ID}")
    print_response(response, "Item Not Found Error")
    print("\n3. Trying to update non-existent item...")
    response = requests.patch(f"{BASE_URL}/inventory/{FAKE_ID}", json={'name': 'Updated Name'})
    print_response(response, "Update Non-Existent Item Error")
    print("\n4. Trying to delete non-existent item...")
    response = requests.delete(f"{BASE_URL}/inventory/{FAKE_ID}")
    print_response(response, "Delete Non-Existent Item Error")

def check_server_status():
    try:
        response = requests.get(f"{BASE_URL}/inventory", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def main():
    print("Inventory Management System - Demo")
    print("This demo showcases all features of the inventory management system")
    if not check_server_status():
        print("\nERROR: Flask server is not running!")
        print("Please start the server with: python app.py")
        return
    print("\nFlask server is running!")
    try:
        demo_basic_operations()
        time.sleep(2)
        demo_search_functionality()
        time.sleep(2)
        demo_openfoodfacts_integration()
        time.sleep(2)
        demo_error_handling()
        print_section("Demo Complete")
        print("All demos completed successfully!")
        print("Try the CLI interface with: python cli.py")
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nDemo failed with error: {e}")

if __name__ == "__main__":
    main()
