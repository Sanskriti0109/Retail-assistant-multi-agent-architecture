from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
import json

from data.products import products, orders
from agents.master_agent import MasterAgent
from agents.inventory_agent import InventoryAgent
from agents.recommendation_agent import RecommendationAgent
from agents.comparison_agent import ComparisonAgent
from agents.memory_agent import MemoryAgent
from agents.post_order_agent import PostOrderAgent

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Initialize all agents
master_agent = MasterAgent()
inventory_agent = InventoryAgent(products)
recommendation_agent = RecommendationAgent(products)
comparison_agent = ComparisonAgent(products)
memory_agent = MemoryAgent()
post_order_agent = PostOrderAgent(orders)

@app.post("/start_session")
async def start_session():
    session_id = str(uuid.uuid4())
    memory_agent.create_session(session_id)
    return {"session_id": session_id}

@app.post("/chat")
async def chat(session_id: str, message: str):
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID required")
    
    # Store user message in memory
    memory_agent.add_message(session_id, "user", message)
    
    # Master agent processes intent
    intent = master_agent.classify_intent(message)
    entities = master_agent.extract_entities(message)
    
    response = {"session_id": session_id, "intent": intent, "entities": entities}
    
    try:
        if intent == "recommend":
            # Get personalized context from memory
            context = memory_agent.get_recommendation_context(session_id)
            
            products_found = recommendation_agent.recommend_by_query(message, entities)
            products_found = inventory_agent.filter_available_products(products_found)
            
            response.update({
                "response": f"Found {len(products_found)} products matching your search!",
                "products": products_found[:5],  # Limit to 5 products
                "suggestions": ["Compare products", "Check stock", "See similar items"]
            })
            
            # Add to browsing history
            for product in products_found[:3]:
                memory_agent.add_to_browsing_history(session_id, product['id'])
        
        elif intent == "compare":
            if 'product_ids' in entities and len(entities['product_ids']) >= 2:
                comparison = comparison_agent.compare_products(entities['product_ids'])
                best_option = comparison_agent.get_best_option(entities['product_ids'])
                
                response.update({
                    "response": f"Comparing {len(entities['product_ids'])} products:",
                    "comparison": comparison,
                    "best_option": best_option,
                    "products": [p for p in products if p['id'] in entities['product_ids']]
                })
            else:
                response["response"] = "Please specify which products to compare (use product IDs like #1, #2)"
        
        elif intent == "inventory":
            if 'product_ids' in entities:
                stock_info = []
                for pid in entities['product_ids']:
                    stock = inventory_agent.check_stock(pid)
                    stock_info.append(stock)
                response.update({
                    "response": "Stock information:",
                    "stock_info": stock_info
                })
            else:
                response["response"] = "Please specify which products to check stock for"
        
        elif intent == "order_status":
            if 'order_id' in entities:
                status = post_order_agent.get_order_status(entities['order_id'])
                tracking = post_order_agent.get_tracking_details(entities['order_id'])
                response.update({
                    "response": f"Order {entities['order_id']} status:",
                    "order_status": status,
                    "tracking_info": tracking
                })
            else:
                response["response"] = "Please provide your order ID (like ORD1001)"
        
        elif intent == "return":
            if 'order_id' in entities:
                # Mock return initiation
                return_request = post_order_agent.initiate_return(
                    entities['order_id'], 
                    entities.get('product_ids', []),
                    "Customer request"
                )
                response.update({
                    "response": "Return request initiated successfully",
                    "return_request": return_request
                })
            else:
                response["response"] = "Please provide your order ID for return processing"
        
        else:
            # General conversation with context
            context = memory_agent.get_conversation_context(session_id, last_n=3)
            response["response"] = "I can help you with product recommendations, comparisons, stock checks, order tracking, and returns. What would you like to do?"
            response["context"] = context
    
    except Exception as e:
        response["response"] = f"Sorry, I encountered an error: {str(e)}"
    
    # Store assistant response in memory
    memory_agent.add_message(session_id, "assistant", response["response"])
    
    return response

@app.get("/product/{product_id}")
async def get_product(product_id: int):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get similar products
    similar_products = recommendation_agent.recommend_similar(product_id)
    stock_info = inventory_agent.check_stock(product_id)
    
    return {
        "product": product,
        "similar_products": similar_products,
        "stock_info": stock_info
    }

@app.get("/order/{order_id}")
async def get_order_details(order_id: str):
    order_status = post_order_agent.get_order_status(order_id)
    if "error" in order_status:
        raise HTTPException(status_code=404, detail=order_status["error"])
    
    return order_status

@app.get("/session/{session_id}/history")
async def get_session_history(session_id: str):
    context = memory_agent.get_conversation_context(session_id)
    preferences = memory_agent.get_preferences(session_id)
    
    return {
        "conversation_history": context,
        "user_preferences": preferences
    }

# Cleanup old sessions periodically
@app.on_event("startup")
async def startup_event():
    memory_agent.cleanup_old_sessions()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)