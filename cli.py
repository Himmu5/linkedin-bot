#!/usr/bin/env python3
"""
LinkedIn Bot CLI - Command line interface for the LinkedIn posting bot
"""

import argparse
import sys
from datetime import datetime, timedelta
from linkedin_bot import LinkedInBot
from content_generator import ContentGenerator
from config import Config
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
    
    # Schedule post command
    schedule_parser = subparsers.add_parser('schedule', help='Schedule a post for a specific date and time')
    schedule_parser.add_argument('--days', '-d', type=int, help='Number of days from now to schedule (e.g., 3 for 3 days from now)')
    schedule_parser.add_argument('--datetime', '-dt', help='Specific date and time (YYYY-MM-DD HH:MM) in your configured timezone')
    schedule_parser.add_argument('--topic', '-t', help='Specific topic to post about')
    
    # List scheduled posts
    list_parser = subparsers.add_parser('list-scheduled', help='List all scheduled posts')
    
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
            # Show next recurring post time
            next_time = bot.get_next_post_time()
            print(f"Next recurring post: {next_time}")
            
            # Show next scheduled post (from scheduled_posts.json)
            next_scheduled = bot.get_next_scheduled_post()
            if next_scheduled:
                scheduled_time = datetime.fromisoformat(next_scheduled['scheduled_time'])
                topic_info = f" (topic: {next_scheduled.get('topic', 'random')})" if next_scheduled.get('topic') else ""
                print(f"\nNext scheduled post: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')} {Config.TIMEZONE}{topic_info}")
                print(f"Post ID: {next_scheduled['id']}")
            else:
                print("\nNo scheduled posts found")
        
        elif args.command == 'schedule':
            tz = Config.get_timezone()
            
            if args.days:
                # Schedule for N days from now at the configured POST_TIME
                post_time_str = Config.POST_TIME
                hours, minutes = map(int, post_time_str.split(':'))
                scheduled_datetime = datetime.now(tz) + timedelta(days=args.days)
                scheduled_datetime = scheduled_datetime.replace(hour=hours, minute=minutes, second=0, microsecond=0)
            elif args.datetime:
                # Parse the provided datetime
                try:
                    scheduled_datetime = datetime.strptime(args.datetime, '%Y-%m-%d %H:%M')
                    scheduled_datetime = tz.localize(scheduled_datetime)
                except ValueError:
                    print("❌ Invalid datetime format. Use: YYYY-MM-DD HH:MM")
                    sys.exit(1)
            else:
                # Default: 3 days from now at POST_TIME
                post_time_str = Config.POST_TIME
                hours, minutes = map(int, post_time_str.split(':'))
                scheduled_datetime = datetime.now(tz) + timedelta(days=3)
                scheduled_datetime = scheduled_datetime.replace(hour=hours, minute=minutes, second=0, microsecond=0)
            
            print(f"Scheduling post for {scheduled_datetime.strftime('%Y-%m-%d %H:%M:%S')} {Config.TIMEZONE}...")
            success = bot.schedule_post(scheduled_datetime, args.topic)
            if success:
                print(f"✅ Post scheduled successfully for {scheduled_datetime.strftime('%Y-%m-%d %H:%M:%S')} {Config.TIMEZONE}!")
                print("Note: Make sure the scheduler is running (use 'python cli.py start') for the post to be published.")
            else:
                print("❌ Failed to schedule post!")
                sys.exit(1)
        
        elif args.command == 'list-scheduled':
            scheduled_posts = bot.get_scheduled_posts()
            if not scheduled_posts:
                print("No scheduled posts found.")
            else:
                print(f"\n📅 Scheduled Posts ({len(scheduled_posts)}):")
                print("="*60)
                for post in scheduled_posts:
                    scheduled_time = datetime.fromisoformat(post['scheduled_time'])
                    print(f"\nID: {post['id']}")
                    print(f"Time: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')} {Config.TIMEZONE}")
                    if post.get('topic'):
                        print(f"Topic: {post['topic']}")
                    print(f"Status: {post.get('status', 'pending')}")
                    print(f"Content preview: {post.get('content', '')[:100]}...")
                print("="*60)
            
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
