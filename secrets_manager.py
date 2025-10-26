"""
Utility module for fetching secrets from Google Cloud Secret Manager
"""
import os
import logging
from typing import Optional, Dict
from google.cloud import secretmanager
from google.api_core import exceptions

logger = logging.getLogger(__name__)

class SecretsManager:
    """Handler for Google Cloud Secret Manager"""
    
    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize the Secrets Manager client
        
        Args:
            project_id: Google Cloud Project ID. If not provided, will use GCP_PROJECT env var
        """
        self.project_id = project_id or os.getenv('GCP_PROJECT')
        self.client = None
        
        if self.project_id:
            try:
                self.client = secretmanager.SecretManagerServiceClient()
                logger.info(f"Secret Manager client initialized for project: {self.project_id}")
            except Exception as e:
                logger.warning(f"Failed to initialize Secret Manager client: {e}")
                self.client = None
        else:
            logger.info("No GCP_PROJECT specified, Secret Manager disabled")
    
    def access_secret(self, secret_id: str, version: str = "latest") -> Optional[str]:
        """
        Access a secret from Secret Manager
        
        Args:
            secret_id: The ID of the secret to access
            version: Version of the secret (default: "latest")
            
        Returns:
            The secret value as a string, or None if not found
        """
        if not self.client or not self.project_id:
            logger.warning("Secret Manager client not initialized")
            return None
        
        try:
            # Build the resource name of the secret version
            name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version}"
            
            # Access the secret version
            response = self.client.access_secret_version(request={"name": name})
            
            # Decode the secret payload
            payload = response.payload.data.decode('UTF-8')
            logger.info(f"Successfully accessed secret: {secret_id}")
            return payload
            
        except exceptions.NotFound:
            logger.error(f"Secret not found: {secret_id}")
            return None
        except exceptions.PermissionDenied:
            logger.error(f"Permission denied accessing secret: {secret_id}")
            return None
        except Exception as e:
            logger.error(f"Error accessing secret {secret_id}: {e}")
            return None
    
    def parse_env_format(self, secret_content: str) -> Dict[str, str]:
        """
        Parse secret content in .env format into a dictionary
        
        Args:
            secret_content: The secret content in KEY=VALUE format
            
        Returns:
            Dictionary of key-value pairs
        """
        env_vars = {}
        
        if not secret_content:
            return env_vars
        
        for line in secret_content.strip().split('\n'):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
        
        return env_vars
    
    def load_secret_to_env(self, secret_id: str, version: str = "latest") -> bool:
        """
        Load a secret from Secret Manager and set as environment variables
        
        Args:
            secret_id: The ID of the secret to access
            version: Version of the secret (default: "latest")
            
        Returns:
            True if successful, False otherwise
        """
        secret_content = self.access_secret(secret_id, version)
        
        if not secret_content:
            logger.warning(f"No content found for secret: {secret_id}")
            return False
        
        # Parse the secret content
        env_vars = self.parse_env_format(secret_content)
        
        if not env_vars:
            logger.warning(f"No variables parsed from secret: {secret_id}")
            return False
        
        # Set environment variables
        for key, value in env_vars.items():
            os.environ[key] = value
            logger.debug(f"Set environment variable: {key}")
        
        logger.info(f"Loaded {len(env_vars)} variables from secret: {secret_id}")
        return True


def load_secrets_from_gcp(secret_id: str = "linkedin-bot", project_id: Optional[str] = None) -> bool:
    """
    Convenience function to load secrets from GCP Secret Manager
    
    Args:
        secret_id: The ID of the secret to access (default: "linkedin-bot")
        project_id: Google Cloud Project ID (optional)
        
    Returns:
        True if successful, False otherwise
    """
    manager = SecretsManager(project_id)
    return manager.load_secret_to_env(secret_id)

