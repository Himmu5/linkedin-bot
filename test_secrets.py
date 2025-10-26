#!/usr/bin/env python3
"""
Test script to verify Secret Manager integration
"""
import os
import sys

def test_local_env():
    """Test loading from .env file"""
    print("=" * 60)
    print("Testing Local .env File Loading")
    print("=" * 60)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    vars_to_check = [
        'LINKEDIN_CLIENT_ID',
        'LINKEDIN_CLIENT_SECRET',
        'GEMINI_API_KEY'
    ]
    
    success = True
    for var in vars_to_check:
        value = os.getenv(var)
        if value:
            # Show first 10 chars for security
            display_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not found")
            success = False
    
    return success

def test_secret_manager():
    """Test loading from Secret Manager"""
    print("\n" + "=" * 60)
    print("Testing GCP Secret Manager Loading")
    print("=" * 60)
    
    # Clear environment first
    vars_to_clear = [
        'LINKEDIN_CLIENT_ID',
        'LINKEDIN_CLIENT_SECRET', 
        'LINKEDIN_ACCESS_TOKEN',
        'GEMINI_API_KEY'
    ]
    for var in vars_to_clear:
        if var in os.environ:
            del os.environ[var]
    
    # Set up for Secret Manager
    project_id = input("\nEnter GCP Project ID (default: citric-celerity-416705): ").strip()
    if not project_id:
        project_id = "citric-celerity-416705"
    
    secret_id = input("Enter Secret ID (default: linkedin-bot): ").strip()
    if not secret_id:
        secret_id = "linkedin-bot"
    
    os.environ['GCP_PROJECT'] = project_id
    os.environ['USE_SECRET_MANAGER'] = 'true'
    os.environ['SECRET_ID'] = secret_id
    
    print(f"\nAttempting to load secret: {secret_id}")
    print(f"From project: {project_id}\n")
    
    try:
        from secrets_manager import load_secrets_from_gcp
        
        if load_secrets_from_gcp(secret_id, project_id):
            print("\n✅ Secrets loaded successfully from Secret Manager!\n")
            
            vars_to_check = [
                'LINKEDIN_CLIENT_ID',
                'LINKEDIN_CLIENT_SECRET',
                'LINKEDIN_ACCESS_TOKEN',
                'GEMINI_API_KEY',
                'POST_TIME',
                'TIMEZONE'
            ]
            
            print("Loaded variables:")
            for var in vars_to_check:
                value = os.getenv(var)
                if value:
                    # Show first 15 chars for security
                    display_value = value[:15] + "..." if len(value) > 15 else value
                    print(f"  ✅ {var}: {display_value}")
                else:
                    print(f"  ⚠️  {var}: Not found")
            
            return True
        else:
            print("\n❌ Failed to load secrets from Secret Manager")
            print("\nPossible issues:")
            print("  1. Secret doesn't exist")
            print("  2. Missing permissions (need secretmanager.secretAccessor role)")
            print("  3. Not authenticated (run: gcloud auth application-default login)")
            return False
            
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("  Make sure google-cloud-secret-manager is installed:")
        print("  pip install google-cloud-secret-manager")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_config_integration():
    """Test the config.py integration"""
    print("\n" + "=" * 60)
    print("Testing config.py Integration")
    print("=" * 60)
    
    # Clear Python module cache
    if 'config' in sys.modules:
        del sys.modules['config']
    
    try:
        from config import Config
        
        print("\nConfig values:")
        print(f"  LINKEDIN_CLIENT_ID: {Config.LINKEDIN_CLIENT_ID[:15] + '...' if Config.LINKEDIN_CLIENT_ID else 'Not set'}")
        print(f"  GEMINI_API_KEY: {Config.GEMINI_API_KEY[:15] + '...' if Config.GEMINI_API_KEY else 'Not set'}")
        print(f"  POST_TIME: {Config.POST_TIME}")
        print(f"  TIMEZONE: {Config.TIMEZONE}")
        
        # Try to validate
        try:
            Config.validate_config()
            print("\n✅ Config validation passed!")
            return True
        except ValueError as e:
            print(f"\n⚠️  Config validation failed: {e}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error loading config: {e}")
        return False

def main():
    print("\n🔐 LinkedIn Bot - Secret Manager Testing Tool\n")
    
    while True:
        print("\nSelect test mode:")
        print("1. Test local .env file")
        print("2. Test GCP Secret Manager")
        print("3. Test config.py integration")
        print("4. Run all tests")
        print("0. Exit")
        
        choice = input("\nEnter choice (0-4): ").strip()
        
        if choice == '0':
            print("\nGoodbye! 👋")
            break
        elif choice == '1':
            test_local_env()
        elif choice == '2':
            test_secret_manager()
        elif choice == '3':
            test_config_integration()
        elif choice == '4':
            print("\n" + "=" * 60)
            print("RUNNING ALL TESTS")
            print("=" * 60)
            
            # Test 1: Local env
            result1 = test_local_env()
            
            # Test 2: Secret Manager
            result2 = test_secret_manager()
            
            # Test 3: Config integration
            result3 = test_config_integration()
            
            print("\n" + "=" * 60)
            print("TEST SUMMARY")
            print("=" * 60)
            print(f"Local .env:         {'✅ PASS' if result1 else '❌ FAIL'}")
            print(f"Secret Manager:     {'✅ PASS' if result2 else '❌ FAIL'}")
            print(f"Config Integration: {'✅ PASS' if result3 else '❌ FAIL'}")
            print()
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye! 👋")
        sys.exit(0)

