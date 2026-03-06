class InventoryAgent:
    def __init__(self, products):
        self.products = products
    
    def check_stock(self, product_id):
        """Check real-time stock for a product"""
        product = next((p for p in self.products if p['id'] == product_id), None)
        if product:
            return {
                "in_stock": product['stock'] > 0,
                "stock_quantity": product['stock'],
                "product_name": product['name']
            }
        return {"in_stock": False, "stock_quantity": 0, "product_name": "Unknown"}
    
    def update_stock(self, product_id, quantity_sold):
        """Update stock after purchase (mock implementation)"""
        product = next((p for p in self.products if p['id'] == product_id), None)
        if product and product['stock'] >= quantity_sold:
            product['stock'] -= quantity_sold
            return True
        return False
    
    def get_low_stock_items(self, threshold=5):
        """Get products with low stock"""
        return [p for p in self.products if p['stock'] <= threshold]
    
    def filter_available_products(self, product_list):
        """Filter out-of-stock products from a list"""
        return [p for p in product_list if p['stock'] > 0]