"""
Production configuration for AI Game Bot
"""
import os

class ProductionConfig:
    """Production configuration class"""
    
    def __init__(self):
        self.config = {
            'HOST': '0.0.0.0',
            'PORT': int(os.environ.get('PORT', 5000)),
            'DEBUG': os.environ.get('DEBUG', 'False').lower() == 'true',
            'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev-secret-key-please-change'),
            'TEMPLATES_AUTO_RELOAD': True,
            'MAX_CONTENT_LENGTH': 16 * 1024 * 1024
        }
    
    def get_flask_config(self):
        """Get Flask configuration dictionary"""
        return self.config

production_config = ProductionConfig()
