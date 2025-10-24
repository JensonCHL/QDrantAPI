#!/usr/bin/env python3
"""
Simple API to retrieve document information from Qdrant
Outputs company as key and list of document sources as values
"""

import os
import json
import sys
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

# Load environment variables
load_dotenv()

# Qdrant Configuration from .env
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

def get_documents_by_company():
    """
    Retrieve all documents from Qdrant and group by company
    Returns a list of dictionaries with company name and document sources
    """
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

def main():
    """Main function to output document information"""
    try:
        documents = get_documents_by_company()
        
        # Output as JSON with the new format
        print(json.dumps({"response": documents}, indent=2))
        
    except Exception as e:
        print(f"Error retrieving documents: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()