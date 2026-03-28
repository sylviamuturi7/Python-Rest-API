# Python REST API with Flask - Inventory Management System

An inventory management system built with Flask that allows employees to add, view by id and delete inventory items.

## Features

- **CRUD Operations**: Create, Read, and Delete functionality for inventory items
- OpenFoodFacts Integration: Function to fetch product details using barcodes
- CLI Interface: Command-line interface for managing inventory
- Unit Testing: Test suite with pytest

## Installation

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Flask Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Using the CLI Interface

Open a new terminal and run:

```bash
python cli.py
```

The CLI provides the following options:
1. Add new item
2. View all inventory
3. View item by ID
4. Update item
5. Delete item
6. Search by barcode
7. Search by name
8. Find product on OpenFoodFacts
9. Exit

### API Endpoints

- `GET /inventory` - Get all inventory items
- `GET /inventory/<id>` - Get a specific inventory item
- `POST /inventory` - Add a new inventory item
- `DELETE /inventory/<id>` - Delete an inventory item

### Request/Response Examples

#### Add New Item
```bash
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Organic Milk",
    "barcode": "123456789",
    "quantity": 20,
    "price": 4.99
  }'
```

#### Get All Items
```bash
curl http://localhost:5000/inventory
```

#### Delete Item
```bash
curl -X DELETE http://localhost:5000/inventory/<item_id>
```

## Data Model

Each inventory item contains:

- `id`: Unique identifier (UUID)
- `name`: Product name
- `barcode`: Product barcode (optional)
- `quantity`: Stock quantity
- `price`: Product price
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## OpenFoodFacts API

This application includes a function to fetch product information from the OpenFoodFacts API using a barcode. The API is called with:
- Custom User-Agent: `InventoryManager/1.0 (test@example.com)`
- Rate limiting: 100 requests/minute for product queries

## Testing

Run the test suite:

```bash
pytest test_app.py -v
```

The test suite covers:
- CRUD operations
- Error handling
- Data validation

## Project Structure

```
Python-Rest-API/
├── app.py              # Flask application with REST API
├── cli.py              # Command-line interface
├── demo.py             # Demo script
├── test_app.py         # Unit tests
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Error Handling

- Validation errors return 400 status
- Not found errors return 404 status

## Development Notes

- Uses in-memory storage (Python list) for simplicity
- All timestamps are in ISO format
- UUIDs are used for item identification

## Future Enhancements

- Persistent database storage (SQLite/PostgreSQL)
- Authentication and authorization
- Search functionality
- Update (PATCH) endpoint
- Web interface

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source and available under the MIT License.
