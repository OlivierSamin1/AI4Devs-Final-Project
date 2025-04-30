#!/usr/bin/env python3
# Database connector for API Bridge

import logging
import psycopg2
from psycopg2 import sql

logger = logging.getLogger('api_bridge.db_connector')

class DatabaseConnector:
    """Database connector for PostgreSQL"""
    
    def __init__(self, host, port, database, user, password):
        """Initialize database connection parameters"""
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
    
    def connect(self):
        """Connect to the database"""
        try:
            if self.connection is None or self.connection.closed:
                logger.info(f"Connecting to database: {self.database} on {self.host}:{self.port}")
                self.connection = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                logger.info("Database connection established")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            return False
    
    def check_connection(self):
        """Check if the database connection is working"""
        try:
            if not self.connect():
                return False
                
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result[0] == 1
        except Exception as e:
            logger.error(f"Database connection check failed: {str(e)}")
            return False
    
    def execute_query(self, query, params=None):
        """Execute a query with optional parameters"""
        if not self.connect():
            raise ConnectionError("Could not connect to database")
        
        try:
            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Check if the query returns data
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    results = cursor.fetchall()
                    # Convert results to list of dictionaries
                    return [dict(zip(columns, row)) for row in results]
                else:
                    self.connection.commit()
                    return {"affected_rows": cursor.rowcount}
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            self.connection.rollback()
            raise
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed") 