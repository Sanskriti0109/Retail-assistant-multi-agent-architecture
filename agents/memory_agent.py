import time
from datetime import datetime, timedelta

class MemoryAgent:
    def __init__(self):
        self.conversations = {}
        self.session_timeout = 3600  # 1 hour
    
    def create_session(self, session_id):
        """Create a new conversation session"""
        self.conversations[session_id] = {
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "messages": [],
            "user_preferences": {},
            "cart": [],
            "browsing_history": [],
            "mentioned_products": []
        }
    
    def add_message(self, session_id, role, content, metadata=None):
        """Add a message to conversation history"""
        if session_id not in self.conversations:
            self.create_session(session_id)
        
        message = {
            "role": role,  # 'user' or 'assistant'
            "content": content,
            "timestamp": datetime.now(),
            "metadata": metadata or {}
        }
        
        self.conversations[session_id]["messages"].append(message)
        self.conversations[session_id]["last_activity"] = datetime.now()
        
        # Clean old messages (keep last 20)
        if len(self.conversations[session_id]["messages"]) > 20:
            self.conversations[session_id]["messages"] = self.conversations[session_id]["messages"][-20:]
    
    def get_conversation_context(self, session_id, last_n=5):
        """Get recent conversation context"""
        if session_id not in self.conversations:
            return []
        
        messages = self.conversations[session_id]["messages"][-last_n:]
        return [{"role": msg["role"], "content": msg["content"]} for msg in messages]
    
    def update_preferences(self, session_id, preferences):
        """Update user preferences based on conversation"""
        if session_id not in self.conversations:
            self.create_session(session_id)
        
        self.conversations[session_id]["user_preferences"].update(preferences)
    
    def get_preferences(self, session_id):
        """Get user preferences"""
        if session_id in self.conversations:
            return self.conversations[session_id]["user_preferences"]
        return {}
    
    def add_to_browsing_history(self, session_id, product_id):
        """Add product to browsing history"""
        if session_id not in self.conversations:
            self.create_session(session_id)
        
        if product_id not in self.conversations[session_id]["browsing_history"]:
            self.conversations[session_id]["browsing_history"].append(product_id)
            # Keep only last 10 products
            self.conversations[session_id]["browsing_history"] = self.conversations[session_id]["browsing_history"][-10:]
    
    def get_recommendation_context(self, session_id):
        """Get context for personalized recommendations"""
        if session_id not in self.conversations:
            return {}
        
        session = self.conversations[session_id]
        return {
            "browsing_history": session["browsing_history"],
            "preferences": session["user_preferences"],
            "recent_interests": self._extract_interests(session["messages"])
        }
    
    def _extract_interests(self, messages):
        """Extract user interests from conversation"""
        interests = set()
        for msg in messages:
            if msg["role"] == "user":
                content = msg["content"].lower()
                if "shirt" in content:
                    interests.add("shirts")
                if "pant" in content or "jeans" in content:
                    interests.add("pants")
                if "formal" in content:
                    interests.add("formal_wear")
                if "casual" in content:
                    interests.add("casual_wear")
                if any(word in content for word in ["cheap", "budget", "affordable"]):
                    interests.add("budget_friendly")
        return list(interests)
    
    def cleanup_old_sessions(self):
        """Remove old sessions to free memory"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session_data in self.conversations.items():
            if current_time - session_data["last_activity"] > timedelta(seconds=self.session_timeout):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.conversations[session_id]