import re

class MasterAgent:
    def __init__(self):
        self.intents = {
            "recommend": ["show", "find", "recommend", "suggest", "looking for", "need"],
            "compare": ["compare", "difference between", "vs", "versus", "which is better"],
            "inventory": ["stock", "available", "inventory", "do you have"],
            "order_status": ["status", "track", "where is my order", "delivery", "tracking"],
            "return": ["return", "refund", "exchange", "not satisfied"],
            "checkout": ["buy", "purchase", "checkout", "cart", "order now"]
        }
    
    def classify_intent(self, message):
        message_lower = message.lower()
        
        for intent, keywords in self.intents.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        return "general"
    
    def extract_entities(self, message):
        entities = {}
        
        # Extract budget
        budget_match = re.search(r'under\s*₹?\s*(\d+)', message.lower())
        if budget_match:
            entities['max_price'] = int(budget_match.group(1))
        
        # Extract categories
        if 'shirt' in message.lower():
            entities['category'] = 'shirts'
        elif any(word in message.lower() for word in ['pant', 'jeans', 'trouser']):
            entities['category'] = 'pants'
        elif 'belt' in message.lower():
            entities['category'] = 'accessories'
            
        # Extract product IDs for comparison
        id_matches = re.findall(r'#?(\d+)', message)
        if id_matches:
            entities['product_ids'] = [int(pid) for pid in id_matches[:3]]  # Max 3 products
        
        # Extract order ID
        order_match = re.search(r'ORD(\d+)', message.upper())
        if order_match:
            entities['order_id'] = f"ORD{order_match.group(1)}"
        
        return entities