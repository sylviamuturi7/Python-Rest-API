# Python REST API with Flask - Inventory Management System

An inventory management system built with Flask that allows employees to add, view by id and delete inventory items.

Features

- **CRUD Operations**: Create, Read, and Delete functionality for inventory items
- OpenFoodFacts Integration: Function to fetch product details by name
- CLI Interface: Command-line interface for managing inventory
- Unit Testing: Test suite with pytest

Installation

3. Install dependencies:
```bash
pip install -r requirements.txt
```

The server will start on `http://localhost:5000`

Using the CLI Interface

Open a new terminal and run:

```bash
python3 cli.py
```

```bash
python3 app.py
```

```bash
python3 demo.py
```

```bash
pytest test_app.py -v
```

The CLI provides the following options:
1. Add new item
2. View all inventory
3. View item by ID
4. Update item
5. Delete item
6. Search by name
7. Find product on OpenFoodFacts
8. Exit

 API Endpoints

- `GET /inventory` - Get all inventory items
- `GET /inventory/<id>` - Get a specific inventory item
- `POST /inventory` - Add a new inventory item
- `DELETE /inventory/<id>` - Delete an inventory item

Request/Response Examples
-Get All Items
```bash
curl http://localhost:5000/inventory
```

Delete Item
```bash
curl -X DELETE http://localhost:5000/inventory/<item_id>
```

Each inventory item contains:

- `id`: Unique identifier (UUID)
- `name`: Product name
- `quantity`: Stock quantity
- `price`: Product price
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

OpenFoodFacts API

This application includes a function to fetch product information from the OpenFoodFacts API. The API is called with:
- Custom User-Agent: `InventoryManager/1.0 (test@example.com)`
- Rate limiting: 100 requests/minute for product queries

 Project Structure

Python-Rest-API/
├── app.py              -Flask application with REST API
├── cli.py              - Command-line interface
├── demo.py             - Demo script
├── test_app.py         - Unit tests
├── requirements.txt    - Python dependencies
└── README.md           

 Error Handling
- Validation errors return 400 status
- Not found errors return 404 status

 Development Notes
- All timestamps are in ISO format
- IDs are used for item identification



