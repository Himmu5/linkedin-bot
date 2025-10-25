import requests
import json
from typing import Dict, Any, Optional
from config import Config

class LinkedInAPI:
    """LinkedIn API integration for posting content"""
    
    def __init__(self):
        self.access_token = Config.LINKEDIN_ACCESS_TOKEN
        self.base_url = Config.LINKEDIN_API_BASE
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
    
    def get_profile_info(self) -> Dict[str, Any]:
        """Get current user's profile information"""
        try:
            # Use the working OpenID Connect endpoint
            response = requests.get(
                'https://api.linkedin.com/v2/userinfo',
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting profile info: {e}")
            return {}
    
    def get_profile_id(self) -> Optional[str]:
        """Get the user's LinkedIn profile ID"""
        profile = self.get_profile_info()
        # OpenID Connect endpoint returns 'sub' field as the user ID
        return profile.get('sub')
    
    def create_text_post(self, text: str) -> Dict[str, Any]:
        """Create a text-only post on LinkedIn"""
        profile_id = self.get_profile_id()
        if not profile_id:
            raise ValueError("Could not retrieve profile ID")
        
        # Prepare the post data
        post_data = {
            "author": f"urn:li:person:{profile_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/ugcPosts',
                headers=self.headers,
                data=json.dumps(post_data)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating post: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            raise
    
    def create_post_with_image(self, text: str, image_url: str) -> Dict[str, Any]:
        """Create a post with an image"""
        profile_id = self.get_profile_id()
        if not profile_id:
            raise ValueError("Could not retrieve profile ID")
        
        # First, register the image
        image_data = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": f"urn:li:person:{profile_id}",
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }
        
        try:
            # Register the image upload
            upload_response = requests.post(
                f'{self.base_url}/assets?action=registerUpload',
                headers=self.headers,
                data=json.dumps(image_data)
            )
            upload_response.raise_for_status()
            upload_data = upload_response.json()
            
            # Upload the image
            upload_url = upload_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            asset_id = upload_data['value']['asset']
            
            # Download and upload the image
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            upload_headers = upload_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['headers']
            upload_headers['Content-Type'] = 'application/octet-stream'
            
            requests.post(upload_url, headers=upload_headers, data=image_response.content)
            
            # Create the post with image
            post_data = {
                "author": f"urn:li:person:{profile_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": [
                            {
                                "status": "READY",
                                "description": {
                                    "text": "Frontend technology insight"
                                },
                                "media": asset_id,
                                "title": {
                                    "text": "Frontend Tech"
                                }
                            }
                        ]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(
                f'{self.base_url}/ugcPosts',
                headers=self.headers,
                data=json.dumps(post_data)
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error creating post with image: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            raise
    
    def test_connection(self) -> bool:
        """Test if the LinkedIn API connection is working"""
        try:
            profile = self.get_profile_info()
            # OpenID Connect endpoint returns 'sub' field as the user ID
            return bool(profile.get('sub'))
        except Exception as e:
            print(f"LinkedIn API connection test failed: {e}")
            return False
