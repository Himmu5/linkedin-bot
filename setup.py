import os
import sys
from pathlib import Path

def setup_environment():
    """Setup environment files and directories"""
    project_root = Path(__file__).parent
    
    # Create .env file if it doesn't exist
    env_file = project_root / '.env'
    env_example = project_root / '.env.example'
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from template...")
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        print("✅ .env file created. Please edit it with your actual credentials.")
    elif env_file.exists():
        print("✅ .env file already exists.")
    else:
        print("❌ .env.example file not found!")
        return False
    
    # Create logs directory
    logs_dir = project_root / 'logs'
    logs_dir.mkdir(exist_ok=True)
    print("✅ Logs directory ready.")
    
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'requests', 'python-dotenv', 'schedule', 'openai', 'pytz'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed.")
        return True

def validate_config():
    """Validate configuration"""
    try:
        from config import Config
        Config.validate_config()
        print("✅ Configuration is valid.")
        return True
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your .env file and ensure all required values are set.")
        return False

def main():
    """Main setup function"""
    print("LinkedIn Bot Setup")
    print("=" * 50)
    
    # Setup environment
    if not setup_environment():
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Validate configuration
    if not validate_config():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your actual credentials")
    print("2. Run 'python oauth_helper.py' to get LinkedIn access token")
    print("3. Run 'python cli.py test' to test the connection")
    print("4. Run 'python cli.py start' to start the daily bot")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
