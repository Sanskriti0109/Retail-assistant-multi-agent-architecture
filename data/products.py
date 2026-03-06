products = [
    {
        "id": 1,
        "name": "Allen Solly Casual Shirt",
        "price": 799,
        "category": "shirts", 
        "description": "Blue casual shirt perfect for office wear, cotton fabric, comfortable fit",
        "stock": 10,
        "size": "M",
        "brand": "Allen Solly",
        "features": ["Cotton", "Machine Wash", "Slim Fit"],
        "colors": ["Blue", "White"],
        "rating": 4.2
    },
    {
        "id": 2, 
        "name": "Van Heusen Formal Shirt",
        "price": 1299,
        "category": "shirts",
        "description": "White formal shirt for business meetings, premium cotton, formal collar",
        "stock": 5,
        "size": "L", 
        "brand": "Van Heusen",
        "features": ["Premium Cotton", "Formal Collar", "Iron Safe"],
        "colors": ["White", "Light Blue"],
        "rating": 4.5
    },
    {
        "id": 3,
        "name": "Peter England Denim Jeans",
        "price": 1599, 
        "category": "pants",
        "description": "Comfortable blue denim jeans, stretchable fabric, modern fit",
        "stock": 8,
        "size": "32",
        "brand": "Peter England",
        "features": ["Stretch Denim", "Machine Wash", "Modern Fit"],
        "colors": ["Blue", "Black"],
        "rating": 4.0
    },
    {
        "id": 4,
        "name": "Louis Philippe Belt", 
        "price": 499,
        "category": "accessories",
        "description": "Genuine leather brown belt, premium finish, durable buckle",
        "stock": 15,
        "size": "M",
        "brand": "Louis Philippe",
        "features": ["Genuine Leather", "Brass Buckle", "Adjustable"],
        "colors": ["Brown", "Black"],
        "rating": 4.3
    },
    {
        "id": 5,
        "name": "Raymond Linen Shirt",
        "price": 1899,
        "category": "shirts",
        "description": "Premium linen shirt for summer, breathable fabric, casual style",
        "stock": 3,
        "size": "L",
        "brand": "Raymond",
        "features": ["Pure Linen", "Breathable", "Casual Style"],
        "colors": ["Beige", "Navy"],
        "rating": 4.7
    }
]

# Mock orders database
orders = {
    "ORD1001": {
        "order_id": "ORD1001",
        "status": "shipped",
        "items": [products[0], products[2]],
        "total": 2398,
        "tracking_number": "TRK789456123",
        "estimated_delivery": "2024-12-28",
        "customer_name": "John Doe",
        "shipping_address": "123 Main St, Mumbai"
    },
    "ORD1002": {
        "order_id": "ORD1002", 
        "status": "delivered",
        "items": [products[1]],
        "total": 1299,
        "tracking_number": "TRK123456789",
        "delivery_date": "2024-12-20",
        "customer_name": "Jane Smith",
        "shipping_address": "456 Oak Ave, Delhi"
    }
}