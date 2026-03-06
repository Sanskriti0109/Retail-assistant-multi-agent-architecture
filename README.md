# ABFRL Conversational Shopping Assistant 
## 🚀 Overview
A production-ready backend system featuring 6 specialized AI agents that power intelligent conversational commerce. Built with FastAPI, local AI processing, and microservices architecture.

## ✨ Features
### 🤖 6 Specialized AI Agents
Agent	Purpose	Technology

Master Agent 🧠	Intent classification & routing	Rule-based NLP

Recommendation Agent 🎯	Product discovery & suggestions	Sentence Transformers + FAISS

Comparison Agent ⚖️	Product feature analysis	Feature scoring algorithms

Inventory Agent 📦	Real-time stock management	Live validation

Memory Agent 💾	Conversation context	Session management

Post-Order Agent 📮	Order tracking & support	Status workflows


## 🎯 Key Capabilities

Local AI Processing - Zero external API dependencies

Semantic Search - FAISS vector similarity for product discovery

Real-time Inventory - Live stock checks and validation

Smart Bundles - AI-powered product combinations

Session Management - Cross-channel conversation memory

Auto-generated API Docs - Interactive Swagger/OpenAPI

## Tech Stack
<img width="892" height="362" alt="Screenshot 2026-03-06 142627" src="https://github.com/user-attachments/assets/a43e37af-fb72-442d-8c42-9a559f4cd4b6" />

Framework: FastAPI (Python 3.12)

AI/ML: Sentence Transformers, FAISS, Scikit-learn

Session Management: In-memory with UUID sessions

API Documentation: Auto-generated Swagger/OpenAPI

Data: Mock product catalog with real-time inventory
<img width="1919" height="1079" alt="Screenshot 2026-03-06 142251" src="https://github.com/user-attachments/assets/64d0ef32-a9e8-4b13-ad11-48c3ebba0acf" />

<img width="1919" height="1079" alt="Screenshot 2026-03-06 142215" src="https://github.com/user-attachments/assets/277ea3f0-b6dc-4a44-913c-4818f46b385f" />


## 🛠️ Installation
Prerequisites
Python 3.8+

pip (Python package manager)

### Clone repository
git clone <repository-url>
cd retail-assistant/backend

### Create virtual environment
python -m venv venv

### Activate virtual environment
### Windows:
venv\Scripts\activate
### Mac/Linux:
source venv/bin/activate

### Install dependencies
pip install -r requirements.txt

### Run the Server
python main.py

## 🤝 Contributing
Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request


