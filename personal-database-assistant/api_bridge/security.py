#!/usr/bin/env python3
# Security handling for API Bridge

import os
import logging
from cryptography.fernet import Fernet

logger = logging.getLogger('api_bridge.security')

class SecureConnection:
    """Handles secure connections and encryption"""
    
    def __init__(self):
        """Initialize the secure connection handler"""
        self.key = None
        self.cipher = None
    
    def setup(self):
        """Set up security features"""
        logger.info("Setting up secure connection")
        self._setup_encryption()
    
    def _setup_encryption(self):
        """Set up encryption for sensitive data"""
        try:
            # Get or generate encryption key
            key_path = os.getenv('ENCRYPTION_KEY_PATH')
            if key_path and os.path.exists(key_path):
                with open(key_path, 'rb') as key_file:
                    self.key = key_file.read()
            else:
                # Generate a new key if none exists
                self.key = Fernet.generate_key()
                if key_path:
                    os.makedirs(os.path.dirname(key_path), exist_ok=True)
                    with open(key_path, 'wb') as key_file:
                        key_file.write(self.key)
            
            # Initialize the cipher
            self.cipher = Fernet(self.key)
            logger.info("Encryption initialized successfully")
        except Exception as e:
            logger.error(f"Failed to set up encryption: {str(e)}")
            raise
    
    def encrypt(self, data):
        """Encrypt data"""
        if not self.cipher:
            raise RuntimeError("Encryption not initialized")
        
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            return self.cipher.encrypt(data)
        except Exception as e:
            logger.error(f"Encryption error: {str(e)}")
            raise
    
    def decrypt(self, data):
        """Decrypt data"""
        if not self.cipher:
            raise RuntimeError("Encryption not initialized")
        
        try:
            decrypted = self.cipher.decrypt(data)
            return decrypted.decode('utf-8')
        except Exception as e:
            logger.error(f"Decryption error: {str(e)}")
            raise

# Create a singleton instance
secure_connection = SecureConnection() 