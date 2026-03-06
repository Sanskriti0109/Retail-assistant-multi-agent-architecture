class ComparisonAgent:
    def __init__(self, products):
        self.products = products
    
    def compare_products(self, product_ids):
        """Compare multiple products feature by feature"""
        products_to_compare = []
        
        for pid in product_ids:
            product = next((p for p in self.products if p['id'] == pid), None)
            if product:
                products_to_compare.append(product)
        
        if len(products_to_compare) < 2:
            return {"error": "Need at least 2 products to compare"}
        
        # Extract comparison features
        comparison = {
            "products": products_to_compare,
            "features_comparison": self._compare_features(products_to_compare),
            "price_comparison": self._compare_prices(products_to_compare),
            "value_analysis": self._analyze_value(products_to_compare)
        }
        
        return comparison
    
    def _compare_features(self, products):
        """Compare features across products"""
        all_features = set()
        for product in products:
            all_features.update(product.get('features', []))
        
        feature_matrix = {}
        for feature in all_features:
            feature_matrix[feature] = []
            for product in products:
                feature_matrix[feature].append(feature in product.get('features', []))
        
        return feature_matrix
    
    def _compare_prices(self, products):
        """Compare prices and identify best value"""
        prices = [p['price'] for p in products]
        min_price = min(prices)
        max_price = max(prices)
        
        return {
            "price_range": f"₹{min_price} - ₹{max_price}",
            "most_expensive": products[prices.index(max_price)]['name'],
            "most_affordable": products[prices.index(min_price)]['name'],
            "price_difference": max_price - min_price
        }
    
    def _analyze_value(self, products):
        """Simple value analysis based on price and features"""
        analysis = []
        for product in products:
            value_score = len(product.get('features', [])) / (product['price'] / 100)
            analysis.append({
                "product_name": product['name'],
                "value_score": round(value_score, 2),
                "features_count": len(product.get('features', [])),
                "price_per_feature": round(product['price'] / max(1, len(product.get('features', []))), 2)
            })
        
        # Sort by value score
        analysis.sort(key=lambda x: x['value_score'], reverse=True)
        return analysis
    
    def get_best_option(self, product_ids, criteria="value"):
        """Get the best product based on criteria"""
        comparison = self.compare_products(product_ids)
        
        if criteria == "value" and "value_analysis" in comparison:
            return comparison["value_analysis"][0]  # Highest value score
        elif criteria == "price":
            prices = [(p['name'], p['price']) for p in comparison["products"]]
            return min(prices, key=lambda x: x[1])
        
        return None