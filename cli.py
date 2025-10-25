#!/usr/bin/env python3
"""
LinkedIn Bot CLI - Command line interface for the LinkedIn posting bot
"""

import argparse
import sys
from linkedin_bot import LinkedInBot
from content_generator import ContentGenerator
import logging

def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def main():
    parser = argparse.ArgumentParser(description='LinkedIn Bot for Frontend Tech Posts')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start bot command
    start_parser = subparsers.add_parser('start', help='Start the daily posting bot')
    
    # Post now command
    post_parser = subparsers.add_parser('post', help='Create and post content immediately')
    post_parser.add_argument('--topic', '-t', help='Specific topic to post about')
    
    # Test connection command
    test_parser = subparsers.add_parser('test', help='Test LinkedIn API connection')
    
    # Generate content command
    generate_parser = subparsers.add_parser('generate', help='Generate content without posting')
    generate_parser.add_argument('--topic', '-t', help='Specific topic to generate content about')
    
    # Show next post time
    next_parser = subparsers.add_parser('next', help='Show next scheduled post time')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    setup_logging(args.verbose)
    
    try:
        bot = LinkedInBot()
        
        if args.command == 'start':
            print("Starting LinkedIn Bot...")
            bot.start_scheduler()
            
        elif args.command == 'post':
            print(f"Creating immediate post{' for topic: ' + args.topic if args.topic else ''}...")
            success = bot.post_now(args.topic)
            if success:
                print("✅ Post created successfully!")
            else:
                print("❌ Post creation failed!")
                sys.exit(1)
                
        elif args.command == 'test':
            print("Testing LinkedIn API connection...")
            success = bot.test_connection()
            if success:
                print("✅ LinkedIn API connection successful!")
            else:
                print("❌ LinkedIn API connection failed!")
                sys.exit(1)
                
        elif args.command == 'generate':
            generator = ContentGenerator()
            topic = args.topic or generator.get_random_topic()
            print(f"Generating content for topic: {topic}")
            content = generator.generate_post(topic)
            print("\n" + "="*50)
            print("GENERATED CONTENT:")
            print("="*50)
            print(content)
            print("="*50)
            
        elif args.command == 'next':
            next_time = bot.get_next_post_time()
            print(f"Next scheduled post: {next_time}")
            
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
