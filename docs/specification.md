# Backend Marketplace Specification

## Overview

This document outlines the specification for a backend marketplace service that supports physical goods across multiple categories. The implementation will be divided into three progressive milestones, each building upon the previous one.

### Technology Stack

- **Language**: Python
- **Package Manager**: Poetry
- **Testing Framework**: pytest
- **Code Formatting**: ruff
- **Database**: SQLite (MVP1), potentially PostgreSQL for later milestones
- **Deployment**: Docker Compose
- **HTTP Server**: Simple HTTP server (Flask or FastAPI)

### Categories Supported

- Electronics
- Home
- Clothing
- Other categories as needed

---

## Milestone 1: Simple MVP

### Core Features

1. **User Management**
   - Basic user registration (buyers and sellers)
   - Simple authentication (no tokens)
   - Prevent duplicate user registrations
   - Support for seller names

2. **Product Catalog**
   - Products with categories, descriptions, pricing
   - Inventory tracking
   - Multi-product support per seller
   - Product active/inactive status

3. **Order Management**
   - Order creation with multiple quantities per item
   - Automatic inventory decrement on order placement
   - Order status tracking (pending, completed)
   - Order failure handling for out-of-stock items

4. **API Endpoints**
   - Separate REST endpoints for buyers and sellers
   - Simple JSON responses
   - No pagination (keep it simple)

### Database Schema

#### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('buyer', 'seller')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Products Table

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    inventory INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES users(id)
);
```

#### Orders Table

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES users(id),
    FOREIGN KEY (seller_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### API Endpoints

#### Buyer Endpoints

**POST /api/buyers/register**
- Register a new buyer
- Body: `{"name": "string", "email": "string"}`
- Response: `{"id": int, "name": "string", "email": "string", "role": "buyer"}`

**POST /api/buyers/login**
- Simple login (no tokens)
- Body: `{"email": "string"}`
- Response: `{"id": int, "name": "string", "email": "string", "role": "buyer"}`

**GET /api/buyers/products**
- Browse all available products
- Query params: `category` (optional)
- Response: `{"products": [{"id": int, "name": "string", "category": "string", "description": "string", "price": float, "inventory": int, "seller_name": "string"}]}`

**GET /api/buyers/products/search**
- Search products by name
- Query params: `q` (search term)
- Response: Same as browse products

**POST /api/buyers/orders**
- Create a new order
- Body: `{"buyer_id": int, "product_id": int, "quantity": int}`
- Response: `{"id": int, "buyer_id": int, "seller_id": int, "product_id": int, "quantity": int, "total_price": float, "status": "pending"}`

**GET /api/buyers/{buyer_id}/orders**
- Get orders for a specific buyer
- Response: `{"orders": [{"id": int, "product_name": "string", "quantity": int, "total_price": float, "status": "string", "created_at": "string"}]}`

#### Seller Endpoints

**POST /api/sellers/register**
- Register a new seller
- Body: `{"name": "string", "email": "string"}`
- Response: `{"id": int, "name": "string", "email": "string", "role": "seller"}`

**POST /api/sellers/login**
- Simple login (no tokens)
- Body: `{"email": "string"}`
- Response: `{"id": int, "name": "string", "email": "string", "role": "seller"}`

**POST /api/sellers/products**
- Add a new product
- Body: `{"seller_id": int, "name": "string", "category": "string", "description": "string", "price": float, "inventory": int}`
- Response: `{"id": int, "name": "string", "category": "string", "description": "string", "price": float, "inventory": int, "is_active": true}`

**PUT /api/sellers/products/{product_id}**
- Update an existing product
- Body: `{"name": "string", "category": "string", "description": "string", "price": float, "inventory": int, "is_active": bool}`
- Response: Updated product object

**GET /api/sellers/{seller_id}/products**
- Get all products for a seller
- Response: `{"products": [product objects]}`

**GET /api/sellers/{seller_id}/orders**
- Get all orders for a seller's products
- Response: `{"orders": [{"id": int, "buyer_name": "string", "product_name": "string", "quantity": int, "total_price": float, "status": "string", "created_at": "string"}]}`

**PUT /api/sellers/orders/{order_id}/status**
- Update order status
- Body: `{"status": "completed"}`
- Response: Updated order object

### Business Logic

1. **Inventory Management**
   - Automatically decrement inventory when orders are placed
   - Prevent orders when inventory is insufficient
   - Return error if requested quantity exceeds available stock

2. **Order Processing**
   - Calculate total price (quantity × unit_price)
   - Orders start with "pending" status
   - Sellers can mark orders as "completed"

3. **Validation Rules**
   - Prevent duplicate email registrations
   - Validate required fields
   - Ensure positive quantities and prices
   - Check seller owns product before updates

### Error Handling

- Return appropriate HTTP status codes
- Standard error response format: `{"error": "string", "message": "string"}`
- Handle common scenarios:
  - User not found
  - Product not found
  - Insufficient inventory
  - Duplicate registration
  - Invalid input data

---

## Milestone 2: Enhanced Features

### Additional Features

1. **Authentication**
   - JWT token-based authentication
   - Protected endpoints
   - Token refresh mechanism

2. **Payment Processing**
   - Integration with payment gateway
   - Payment status tracking
   - Order payment validation

3. **CLI Application for Sellers**
   - Command-line interface for sellers
   - Add/update products
   - View orders and inventory
   - Manage product status

4. **Enhanced Order Management**
   - Extended order statuses (processing, shipped, delivered, cancelled)
   - Order cancellation functionality
   - Order history tracking

5. **Product Enhancements**
   - Product images support
   - Product reviews and ratings
   - Product search improvements

### Database Schema Updates

#### Payments Table
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

#### Product Reviews Table
```sql
CREATE TABLE product_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (buyer_id) REFERENCES users(id)
);
```

---

## Milestone 3: Advanced UI

### Additional Features

1. **TUI for Buyers**
   - Terminal-based user interface
   - Product browsing and searching
   - Order placement and tracking
   - Interactive navigation

2. **Advanced Order Tracking**
   - Real-time order status updates
   - Shipping information
   - Delivery tracking
   - Order history with details

3. **Seller Analytics**
   - Sales reporting
   - Inventory analytics
   - Product performance metrics
   - Revenue tracking

4. **Enhanced Search and Filtering**
   - Advanced product filters
   - Price range filtering
   - Category-based browsing
   - Sorting options

### Database Schema Updates

#### Order Tracking Table
```sql
CREATE TABLE order_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,
    location VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

---

## Implementation Details

### Project Structure

```
backend-marketplace/
├── docs/
│   └── specification.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── buyers.py
│   │   └── sellers.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── migrations.py
│   └── utils/
│       ├── __init__.py
│       └── validation.py
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_products.py
│   └── test_orders.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── .gitignore
```

### Testing Strategy

- Unit tests for all models and API endpoints
- Integration tests for complete workflows
- Test database setup and teardown
- Mock external dependencies
- Coverage reporting

### Deployment

#### Docker Compose Configuration
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - database
    environment:
      - DATABASE_URL=sqlite:///./marketplace.db
  
  database:
    image: sqlite:latest
    volumes:
      - ./data:/data
```

### Development Workflow

1. Set up Poetry environment
2. Install dependencies
3. Run database migrations
4. Start development server
5. Run tests with pytest
6. Format code with ruff
7. Build and test with Docker

This specification provides a comprehensive roadmap for implementing the backend marketplace service across three progressive milestones, ensuring a solid foundation that can be extended with additional features over time.