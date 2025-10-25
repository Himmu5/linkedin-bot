import os
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Load environment variables
load_dotenv()

class Config:
    # LinkedIn API Configuration
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    LINKEDIN_REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:8080/callback')
    LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
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
            'OPENAI_API_KEY'
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
