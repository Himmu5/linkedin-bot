#!/usr/bin/env python3
"""
LinkedIn OAuth Helper - Helper script to get LinkedIn access token
"""

import webbrowser
import urllib.parse
import requests
import json
from config import Config

def get_authorization_url():
    """Generate LinkedIn authorization URL"""
    params = {
        'response_type': 'code',
        'client_id': Config.LINKEDIN_CLIENT_ID,
        'redirect_uri': Config.LINKEDIN_REDIRECT_URI,
        'state': 'random_state_string',
        'scope': 'r_liteprofile w_member_social'
    }
    
    auth_url = Config.LINKEDIN_AUTH_URL + '?' + urllib.parse.urlencode(params)
    return auth_url

def exchange_code_for_token(authorization_code):
    """Exchange authorization code for access token"""
    token_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': Config.LINKEDIN_REDIRECT_URI,
        'client_id': Config.LINKEDIN_CLIENT_ID,
        'client_secret': Config.LINKEDIN_CLIENT_SECRET
    }
    
    response = requests.post(Config.LINKEDIN_TOKEN_URL, data=token_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def main():
    print("LinkedIn OAuth Helper")
    print("=" * 50)
    
    # Check if credentials are set
    if not Config.LINKEDIN_CLIENT_ID or not Config.LINKEDIN_CLIENT_SECRET:
        print("❌ LinkedIn Client ID and Client Secret must be set in .env file")
        print("Please add them to your .env file:")
        print("LINKEDIN_CLIENT_ID=your_client_id")
        print("LINKEDIN_CLIENT_SECRET=your_client_secret")
        return
    
    print("1. Opening LinkedIn authorization page...")
    auth_url = get_authorization_url()
    print(f"Authorization URL: {auth_url}")
    
    try:
        webbrowser.open(auth_url)
        print("✅ Browser opened. Please authorize the application.")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print(f"Please manually open this URL: {auth_url}")
    
    print("\n2. After authorization, you'll be redirected to a page with an error.")
    print("   Copy the 'code' parameter from the URL.")
    
    authorization_code = input("\nEnter the authorization code: ").strip()
    
    if not authorization_code:
        print("❌ No authorization code provided")
        return
    
    print("\n3. Exchanging code for access token...")
    token_response = exchange_code_for_token(authorization_code)
    
    if token_response and 'access_token' in token_response:
        access_token = token_response['access_token']
        print("✅ Access token obtained successfully!")
        print(f"\nAdd this to your .env file:")
        print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
        
        # Test the token
        print("\n4. Testing the access token...")
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        test_response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
        if test_response.status_code == 200:
            profile = test_response.json()
            print(f"✅ Token is valid! Connected as: {profile.get('name', '')}")
        else:
            print(f"❌ Token test failed: {test_response.status_code} - {test_response.text}")
    else:
        print("❌ Failed to obtain access token")

if __name__ == "__main__":
    main()
