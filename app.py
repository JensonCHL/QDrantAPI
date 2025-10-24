#!/usr/bin/env python3
"""
REST API to retrieve document information from Qdrant
Outputs company as key and list of document sources as values
"""

import os
import json
import sys
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import secrets

# Load environment variables explicitly from .env file
load_dotenv('.env')

# Qdrant Configuration from .env
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

# API Key for authentication
API_KEY = os.getenv("DOCUMENT_API_KEY")

# Debug: Print API key status
print(f"API Key loaded: {'Yes' if API_KEY else 'No'}")
if API_KEY:
    print(f"API Key: {API_KEY[:5]}...{API_KEY[-5:]}")  # Show first 5 and last 5 chars

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def require_api_key(f):
    """Decorator to require API key for protected endpoints"""
    def decorated_function(*args, **kwargs):
        # Skip API key check for health endpoint
        if request.endpoint == 'health_check':
            return f(*args, **kwargs)
        
        # Debug information
        print(f"Request endpoint: {request.endpoint}")
        print(f"API_KEY from env: {'Set' if API_KEY else 'Not set'}")
        
        key = request.headers.get('X-API-Key') or request.args.get('api_key')
        print(f"Provided key: {'Present' if key else 'Missing'}")
        if key:
            print(f"Key comparison: {key == API_KEY}")
        
        if not key or key != API_KEY:
            print("Authentication failed - aborting")
            abort(401, description="Unauthorized: Invalid or missing API key")
        print("Authentication successful")
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def get_documents_by_company():
    """
    Retrieve all documents from Qdrant and group by company
    Returns a list of dictionaries with company name and document sources
    """
    try:
        # Connect to Qdrant
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        
        # Scroll through all points in the collection
        pts, _ = client.scroll(
            collection_name=QDRANT_COLLECTION,
            limit=10000,  # Adjust as needed
            with_payload=True,
            with_vectors=False
        )
        
        # Group documents by company
        company_documents = {}
        
        for p in pts or []:
            meta = (p.payload or {}).get("metadata", {})
            source = meta.get("source", "Unknown Source")
            company = meta.get("company", "Unknown Company")
            
            # Add source to company's document list
            if company not in company_documents:
                company_documents[company] = []
            
            if source not in company_documents[company]:
                company_documents[company].append(source)
        
        # Convert to the new simplified format
        result = []
        for company, sources in company_documents.items():
            company_data = {
                "Company Name": company,
                "Contract Title": ", ".join(sources)  # Join all sources with comma and space
            }
            result.append(company_data)
        
        return result
    except Exception as e:
        raise Exception(f"Error retrieving documents: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint - no authentication required"""
    return jsonify({"status": "healthy", "service": "document-api"}), 200

@app.route('/documents', methods=['GET'])
@require_api_key
def get_documents():
    """Get all documents grouped by company"""
    try:
        documents = get_documents_by_company()
        return jsonify(documents), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/documents/<company_name>', methods=['GET'])
@require_api_key
def get_documents_by_company_name(company_name):
    """Get documents for a specific company"""
    try:
        documents = get_documents_by_company()
        # Find the specific company in the list
        company_data = [item for item in documents if item.get("Company Name") == company_name]
        if company_data:
            return jsonify(company_data), 200
        else:
            return jsonify({"error": f"No documents found for company: {company_name}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
@require_api_key
def home():
    """Home endpoint with API information"""
    return jsonify({
        "message": "Document API Service",
        "endpoints": {
            "GET /": "This information page",
            "GET /health": "Health check",
            "GET /documents": "Get all documents grouped by company",
            "GET /documents/<company_name>": "Get documents for a specific company"
        }
    }), 200

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    # Get host from environment variable or default to localhost
    host = os.getenv('HOST', '127.0.0.1')
    
    print(f"Starting Document API server on {host}:{port}")
    app.run(host=host, port=port, debug=False)