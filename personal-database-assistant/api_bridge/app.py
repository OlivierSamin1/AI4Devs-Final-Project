#!/usr/bin/env python3
# Basic API Bridge application

import os
import json
import logging
import requests
from dotenv import load_dotenv
from db_connector import DatabaseConnector
from security import secure_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('api_bridge')

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the API Bridge service"""
    logger.info("Starting API Bridge service")
    
    # Initialize database connection
    db = DatabaseConnector(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'health_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '')
    )
    
    # Initialize secure connection
    secure_connection.setup()
    
    # Start the API service
    start_api_service(db)

def start_api_service(db):
    """Start the API service with the given database connection"""
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        db_status = db.check_connection()
        return jsonify({
            'status': 'healthy' if db_status else 'unhealthy',
            'database': db_status
        }), 200 if db_status else 503
    
    @app.route('/query', methods=['POST'])
    def query_data():
        """Handle queries from the backend"""
        data = request.json
        if not data or 'query' not in data:
            return jsonify({'error': 'Invalid request'}), 400
        
        try:
            # Execute the query
            query_result = db.execute_query(data['query'])
            return jsonify({'result': query_result}), 200
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    app.run(host='0.0.0.0', port=int(os.getenv('API_BRIDGE_PORT', '5000')))

if __name__ == '__main__':
    main() 