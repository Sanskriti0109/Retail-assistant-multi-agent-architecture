import random
from datetime import datetime, timedelta

class PostOrderAgent:
    def __init__(self, orders_data):
        self.orders = orders_data
        self.order_status_flow = [
            "confirmed",
            "processing", 
            "shipped",
            "out_for_delivery",
            "delivered"
        ]
    
    def get_order_status(self, order_id):
        """Get current status of an order"""
        order = self.orders.get(order_id)
        if not order:
            return {"error": f"Order {order_id} not found"}
        
        status_info = {
            "order_id": order_id,
            "status": order["status"],
            "items": order["items"],
            "total": order["total"],
            "customer_name": order.get("customer_name", "Customer")
        }
        
        # Add status-specific information
        if order["status"] == "shipped":
            status_info.update({
                "tracking_number": order["tracking_number"],
                "estimated_delivery": order["estimated_delivery"]
            })
        elif order["status"] == "delivered":
            status_info.update({
                "delivery_date": order["delivery_date"],
                "tracking_number": order["tracking_number"]
            })
        
        return status_info
    
    def get_tracking_details(self, order_id):
        """Get detailed tracking information"""
        order = self.orders.get(order_id)
        if not order:
            return {"error": f"Order {order_id} not found"}
        
        # Generate mock tracking events based on status
        tracking_events = self._generate_tracking_events(order["status"])
        
        return {
            "order_id": order_id,
            "tracking_number": order.get("tracking_number", "TRK" + str(random.randint(100000, 999999))),
            "current_status": order["status"],
            "events": tracking_events,
            "customer_name": order.get("customer_name", "Customer")
        }
    
    def _generate_tracking_events(self, current_status):
        """Generate mock tracking events based on current status"""
        events = []
        base_date = datetime.now() - timedelta(days=3)
        
        status_index = self.order_status_flow.index(current_status) if current_status in self.order_status_flow else 0
        
        for i, status in enumerate(self.order_status_flow[:status_index + 1]):
            event_date = base_date + timedelta(days=i)
            events.append({
                "status": status,
                "timestamp": event_date.strftime("%Y-%m-%d %H:%M"),
                "description": self._get_status_description(status),
                "location": "Mumbai Warehouse" if i < 2 else "Local Facility"
            })
        
        return events
    
    def _get_status_description(self, status):
        """Get human-readable status description"""
        descriptions = {
            "confirmed": "Order confirmed and payment processed",
            "processing": "Item is being prepared for shipment",
            "shipped": "Item has been shipped from warehouse",
            "out_for_delivery": "Item is out for delivery",
            "delivered": "Item has been delivered successfully"
        }
        return descriptions.get(status, "Status update")
    
    def initiate_return(self, order_id, product_ids, reason):
        """Initiate return process for items"""
        order = self.orders.get(order_id)
        if not order:
            return {"error": f"Order {order_id} not found"}
        
        return_request_id = f"RET{random.randint(1000, 9999)}"
        
        return {
            "return_request_id": return_request_id,
            "order_id": order_id,
            "status": "return_initiated",
            "products": [pid for pid in product_ids],
            "reason": reason,
            "instructions": "Please keep the items in original packaging. Our executive will contact you within 24 hours for pickup.",
            "refund_amount": sum(item['price'] for item in order['items'] if item['id'] in product_ids)
        }
    
    def get_order_history(self, customer_name):
        """Get order history for a customer"""
        customer_orders = []
        for order_id, order in self.orders.items():
            if order.get("customer_name") == customer_name:
                customer_orders.append({
                    "order_id": order_id,
                    "date": order.get("order_date", "2024-12-15"),
                    "status": order["status"],
                    "total": order["total"],
                    "items_count": len(order["items"])
                })
        
        return sorted(customer_orders, key=lambda x: x["date"], reverse=True)