import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)

# Load environment variables
# Priority: 1. GCP Secret Manager, 2. .env file
def load_environment():
    """Load environment variables from Secret Manager or .env file"""
    
    # Check if running in GCP (Cloud Run, Cloud Functions, GCE, etc.)
    is_cloud_environment = os.getenv('K_SERVICE') or os.getenv('FUNCTION_TARGET') or os.getenv('GAE_INSTANCE')
    
    if is_cloud_environment or os.getenv('USE_SECRET_MANAGER', '').lower() == 'true':
        # Running in cloud or explicitly requested to use Secret Manager
        logger.info("Attempting to load secrets from GCP Secret Manager...")
        try:
            from secrets_manager import load_secrets_from_gcp
            
            secret_id = os.getenv('SECRET_ID', 'linkedin-bot')
            project_id = os.getenv('GCP_PROJECT')
            
            if load_secrets_from_gcp(secret_id, project_id):
                logger.info("Successfully loaded secrets from GCP Secret Manager")
                return
            else:
                logger.warning("Failed to load from Secret Manager, falling back to .env file")
        except ImportError:
            logger.warning("secrets_manager module not available, falling back to .env file")
        except Exception as e:
            logger.warning(f"Error loading from Secret Manager: {e}, falling back to .env file")
    
    # Fall back to .env file for local development
    logger.info("Loading environment variables from .env file")
    load_dotenv()

load_environment()

class Config:
    # LinkedIn API Configuration
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    LINKEDIN_REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:8080/callback')
    LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')
    
    # AI Model Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Bot Configuration
    POST_TIME = os.getenv('POST_TIME', '09:00')
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')
    
    # LinkedIn API URLs
    LINKEDIN_API_BASE = 'https://api.linkedin.com/v2'
    LINKEDIN_AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
    LINKEDIN_TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        required_vars = [
            'LINKEDIN_CLIENT_ID',
            'LINKEDIN_CLIENT_SECRET', 
            'LINKEDIN_ACCESS_TOKEN',
            'GEMINI_API_KEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
    
    @classmethod
    def get_timezone(cls):
        """Get timezone object"""
        return pytz.timezone(cls.TIMEZONE)
