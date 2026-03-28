#!/usr/bin/env python3
"""
CLI Interface for Inventory Management System
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def print_menu():
    print("\n=== Inventory Management System ===")
    print("1. Add new item")
    print("2. View all inventory")
    print("3. View item by ID")
    print("4. Update item")
    print("5. Delete item")
    print("6. Search by barcode")
    print("7. Search by name")
    print("8. Find product on OpenFoodFacts")
    print("9. Exit")
    print("=" * 35)

def validate_item_id(item_id):
    if not all(c.isalnum() or c == '-' for c in item_id):
        print("Error: Invalid item ID")
        return False
    return True

def validate_barcode(barcode):
    if not barcode.isdigit():
        print("Error: Invalid barcode")
        return False
    return True

def get_item_input():
    name = input("Enter product name: ")
    if not name:
        print("Error: Name is required")
        return None
    barcode = input("Enter barcode (optional): ") or None
    try:
        quantity = int(input("Enter quantity: ") or "0")
        price = float(input("Enter price: ") or "0.0")
    except ValueError:
        print("Error: Invalid quantity or price")
        return None
    return name, barcode, quantity, price

def print_item(item):
    print(f"ID: {item['id']}")
    print(f"Name: {item['name']}")
    print(f"Barcode: {item.get('barcode', 'N/A')}")
    print(f"Quantity: {item['quantity']}")
    print(f"Price: ${item['price']:.2f}")

def print_product_details(details):
    print(f"\n--- Product Details ---")
    print(f"Product Name: {details.get('product_name', 'N/A')}")
    print(f"Brand: {details.get('brands', 'N/A')}")
    print(f"Ingredients: {details.get('ingredients_text', 'N/A')[:100]}...")
    print(f"Categories: {details.get('categories', 'N/A')}")
    print(f"Nutri-Score: {details.get('nutriscore_grade', 'N/A')}")

def get_update_fields(current_item):
    update_data = {}
    new_name = input(f"Name [{current_item['name']}]: ")
    if new_name:
        update_data['name'] = new_name
    new_barcode = input(f"Barcode [{current_item.get('barcode', 'N/A')}]: ")
    if new_barcode:
        update_data['barcode'] = new_barcode
    new_quantity = input(f"Quantity [{current_item['quantity']}]: ")
    if new_quantity:
        try:
            update_data['quantity'] = int(new_quantity)
        except ValueError:
            print("Error: Invalid quantity")
            return None
    new_price = input(f"Price [{current_item['price']}]: ")
    if new_price:
        try:
            if new_price.lower() == 'nan':
                raise ValueError
            update_data['price'] = float(new_price)
        except ValueError:
            print("Error: Invalid price")
            return None
    return update_data

def add_item():
    print("\n--- Add New Item ---")
    result = get_item_input()
    if not result:
        return
    name, barcode, quantity, price = result
    data = {'name': name, 'quantity': quantity, 'price': price}
    if barcode:
        data['barcode'] = barcode
    try:
        response = requests.post(f"{BASE_URL}/inventory", json=data)
        if response.status_code == 201:
            item = response.json()
            print(f"\nItem added successfully!")
            print_item(item)
            if item.get('product_details'):
                print(f"Product details: {item['product_details'].get('product_name', 'N/A')}")
        else:
            print(f"Error adding item: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def view_all_inventory():
    print("\n--- All Inventory Items ---")
    try:
        response = requests.get(f"{BASE_URL}/inventory")
        if response.status_code == 200:
            items = response.json()
            if not items:
                print("No items in inventory")
                return
            print(f"\nFound {len(items)} items:")
            print("-" * 80)
            for item in items:
                print_item(item)
                if item.get('product_details'):
                    details = item['product_details']
                    print(f"Brand: {details.get('brands', 'N/A')}")
                    print(f"Categories: {details.get('categories', 'N/A')}")
                print("-" * 80)
        else:
            print(f"Error fetching inventory: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def view_item_by_id():
    item_id = input("\nEnter item ID: ")
    if not item_id or not validate_item_id(item_id):
        return
    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        if response.status_code == 200:
            item = response.json()
            print(f"\n--- Item Details ---")
            print_item(item)
            print(f"Created: {item['created_at']}")
            print(f"Updated: {item['updated_at']}")
            if item.get('product_details'):
                print_product_details(item['product_details'])
        else:
            print(f"Error: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def update_item():
    item_id = input("\nEnter item ID to update: ")
    if not item_id or not validate_item_id(item_id):
        return
    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        if response.status_code != 200:
            print(f"Item not found")
            return
        current_item = response.json()
        print(f"\n--- Current Item Details ---")
        print_item(current_item)
        print("\n--- Enter New Values (leave blank to keep current) ---")
        update_data = get_update_fields(current_item)
        if update_data is None:
            return
        if not update_data:
            print("No changes made")
            return
        response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=update_data)
        if response.status_code == 200:
            updated_item = response.json()
            print(f"\nItem updated successfully!")
            print_item(updated_item)
        else:
            print(f"Error updating item: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def delete_item():
    item_id = input("\nEnter item ID to delete: ")
    if not item_id or not validate_item_id(item_id):
        return
    confirm = input(f"Are you sure you want to delete item {item_id}? (y/N): ")
    if confirm.lower() != 'y':
        print("Deletion cancelled")
        return
    try:
        response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"\nItem deleted successfully!")
            print(f"Deleted item: {result['deleted_item']['name']}")
        else:
            print(f"Error deleting item: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def print_barcode_result(result):
    if 'id' in result:
        print(f"\nItem found in inventory!")
        print_item(result)
        if result.get('product_details'):
            print(f"Brand: {result['product_details'].get('brands', 'N/A')}")
    else:
        print(f"\nProduct found in OpenFoodFacts but not in inventory!")
        details = result['product_details']
        print(f"Product Name: {details.get('product_name', 'N/A')}")
        print(f"Brand: {details.get('brands', 'N/A')}")
        print(f"Categories: {details.get('categories', 'N/A')}")
        print(f"Would you like to add this to inventory?")

def search_by_barcode():
    barcode = input("\nEnter barcode to search: ")
    if not barcode or not validate_barcode(barcode):
        return
    try:
        response = requests.get(f"{BASE_URL}/inventory/search/barcode/{barcode}")
        if response.status_code == 200:
            print_barcode_result(response.json())
        else:
            print(f"Product not found")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def search_by_name():
    name = input("\nEnter name to search: ")
    if not name:
        print("Error: Name is required")
        return
    name = name.replace('/', '').replace('\\', '').strip()
    try:
        response = requests.get(f"{BASE_URL}/inventory/search/name/{name}")
        if response.status_code == 200:
            items = response.json()
            if not items:
                print("No items found")
                return
            print(f"\nFound {len(items)} items:")
            print("-" * 60)
            for item in items:
                print_item(item)
                print("-" * 60)
        else:
            print(f"Error searching: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def find_product_on_api():
    barcode = input("\nEnter barcode to search on OpenFoodFacts: ")
    if not barcode or not validate_barcode(barcode):
        return
    try:
        response = requests.get(f"{BASE_URL}/inventory/search/barcode/{barcode}")
        if response.status_code == 200:
            result = response.json()
            if 'product_details' in result:
                print(f"\nProduct Details from OpenFoodFacts:")
                details = result['product_details']
                print(f"Product Name: {details.get('product_name', 'N/A')}")
                print(f"Brand: {details.get('brands', 'N/A')}")
                print(f"Categories: {details.get('categories', 'N/A')}")
                print(f"Ingredients: {details.get('ingredients_text', 'N/A')[:200]}...")
                print(f"Nutri-Score: {details.get('nutriscore_grade', 'N/A')}")
                print(f"NOVA Group: {details.get('nova_group', 'N/A')}")
                print(f"Eco-Score: {details.get('ecoscore_grade', 'N/A')}")
            else:
                print("Product not found in OpenFoodFacts")
        else:
            print(f"Product not found")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def handle_choice(choice):
    actions = {
        '1': add_item,
        '2': view_all_inventory,
        '3': view_item_by_id,
        '4': update_item,
        '5': delete_item,
        '6': search_by_barcode,
        '7': search_by_name,
        '8': find_product_on_api,
    }
    if choice in actions:
        actions[choice]()
    elif choice == '9':
        print("\nGoodbye!")
        return False
    else:
        print("Invalid choice. Please try again.")
    return True

def main():
    print("Welcome to Inventory Management System!")
    print("Make sure the Flask server is running on http://localhost:5000")
    while True:
        print_menu()
        choice = input("Enter your choice (1-9): ")
        if not handle_choice(choice):
            break
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
