from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationAgent:
    def __init__(self, products):
        self.products = products
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self._build_product_embeddings()
    
    def _build_product_embeddings(self):
        """Create embeddings for all products"""
        product_texts = []
        for product in self.products:
            text = f"{product['name']} {product['description']} {product['category']} {product['brand']} {' '.join(product['features'])}"
            product_texts.append(text)
        
        self.embeddings = self.model.encode(product_texts)
        self.product_map = {i: product['id'] for i, product in enumerate(self.products)}
    
    def recommend_similar(self, product_id, top_k=3):
        """Recommend similar products based on product ID"""
        product_idx = next(i for i, p in enumerate(self.products) if p['id'] == product_id)
        
        # Calculate similarities
        similarities = cosine_similarity(
            [self.embeddings[product_idx]], 
            self.embeddings
        )[0]
        
        # Get top similar products (excluding the input product itself)
        similar_indices = np.argsort(similarities)[::-1][1:top_k+1]
        
        similar_products = []
        for idx in similar_indices:
            if similarities[idx] > 0.3:  # Similarity threshold
                product = next(p for p in self.products if p['id'] == self.product_map[idx])
                similar_products.append({
                    **product,
                    "similarity_score": float(similarities[idx])
                })
        
        return similar_products
    
    def recommend_by_query(self, query, filters=None, top_k=5):
        """Recommend products based on text query"""
        if filters is None:
            filters = {}
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Rank products
        ranked_indices = np.argsort(similarities)[::-1]
        
        results = []
        for idx in ranked_indices:
            product = next(p for p in self.products if p['id'] == self.product_map[idx])
            
            # Apply filters
            if self._passes_filters(product, filters):
                results.append({
                    **product,
                    "relevance_score": float(similarities[idx])
                })
            
            if len(results) >= top_k:
                break
        
        return results
    
    def _passes_filters(self, product, filters):
        """Check if product passes all filters"""
        if 'max_price' in filters and product['price'] > filters['max_price']:
            return False
        if 'category' in filters and product['category'] != filters['category']:
            return False
        if 'min_rating' in filters and product.get('rating', 0) < filters['min_rating']:
            return False
        if product['stock'] <= 0:
            return False
        return True