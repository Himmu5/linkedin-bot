import schedule
import time
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from config import Config
from linkedin_api import LinkedInAPI
from content_generator import ContentGenerator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LinkedInBot:
    """Main bot class for automated LinkedIn posting"""
    
    def __init__(self):
        self.linkedin_api = LinkedInAPI()
        self.content_generator = ContentGenerator()
        logger.info(f"LinkedInBot initialized with model: {self.content_generator.model_name}")
        self.is_running = False
        self.scheduled_posts_file = 'scheduled_posts.json'
        
        # Validate configuration
        try:
            Config.validate_config()
            logger.info("Configuration validated successfully")
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test LinkedIn API connection"""
        logger.info("Testing LinkedIn API connection...")
        success = self.linkedin_api.test_connection()
        if success:
            logger.info("LinkedIn API connection successful")
        else:
            logger.error("LinkedIn API connection failed")
        return success
    
    def create_and_post(self, topic: Optional[str] = None) -> bool:
        """Generate content and post to LinkedIn"""
        try:
            logger.info("Starting post creation process...")
            
            # Generate content
            logger.info(f"Generating content for topic: {topic or 'random'} using model: {self.content_generator.model_name}")
            content = self.content_generator.generate_post(topic)
            logger.info(f"Generated content using model '{self.content_generator.model_name}': {content[:100]}...")
            
            # Post to LinkedIn
            logger.info("Posting to LinkedIn...")
            result = self.linkedin_api.create_text_post(content)
            
            if result:
                logger.info("Post created successfully!")
                logger.info(f"Post ID: {result.get('id', 'Unknown')}")
                return True
            else:
                logger.error("Failed to create post")
                return False
                
        except Exception as e:
            logger.error(f"Error in create_and_post: {e}")
            return False
    
    def scheduled_post(self):
        """Scheduled post function"""
        logger.info("Executing scheduled post...")
        success = self.create_and_post()
        
        if success:
            logger.info("Scheduled post completed successfully")
        else:
            logger.error("Scheduled post failed")
    
    def start_scheduler(self):
        """Start the daily posting scheduler"""
        if not self.test_connection():
            logger.error("Cannot start scheduler - LinkedIn API connection failed")
            return False
        
        # Schedule daily posts
        schedule.every().day.at(Config.POST_TIME).do(self.scheduled_post)
        
        # Check for scheduled posts every minute
        schedule.every(1).minutes.do(self._check_and_execute_scheduled_posts)
        
        logger.info(f"Scheduler started - posts will be made daily at {Config.POST_TIME} {Config.TIMEZONE}")
        logger.info("Also checking for scheduled posts every minute")
        
        # Log the next scheduled post
        self._log_next_scheduled_post()
        
        logger.info("Bot is running. Press Ctrl+C to stop.")
        
        self.is_running = True
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            self.stop_scheduler()
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.is_running = False
        schedule.clear()
        logger.info("Scheduler stopped")
    
    def post_now(self, topic: Optional[str] = None) -> bool:
        """Create and post content immediately"""
        logger.info("Creating immediate post...")
        return self.create_and_post(topic)
    
    def get_next_post_time(self) -> str:
        """Get the next scheduled post time"""
        next_run = schedule.next_run()
        if next_run:
            return next_run.strftime("%Y-%m-%d %H:%M:%S")
        return "No posts scheduled"
    
    def _load_scheduled_posts(self) -> List[Dict]:
        """Load scheduled posts from file"""
        if not os.path.exists(self.scheduled_posts_file):
            return []
        try:
            with open(self.scheduled_posts_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error loading scheduled posts: {e}")
            return []
    
    def _save_scheduled_posts(self, posts: List[Dict]):
        """Save scheduled posts to file"""
        try:
            with open(self.scheduled_posts_file, 'w') as f:
                json.dump(posts, f, indent=2)
        except IOError as e:
            logger.error(f"Error saving scheduled posts: {e}")
    
    def schedule_post(self, post_datetime: datetime, topic: Optional[str] = None) -> bool:
        """Schedule a post for a specific date and time"""
        try:
            # Ensure datetime is timezone-aware
            if post_datetime.tzinfo is None:
                tz = Config.get_timezone()
                post_datetime = tz.localize(post_datetime)
            
            # Check if the datetime is in the future
            now = datetime.now(Config.get_timezone())
            if post_datetime <= now:
                logger.error(f"Cannot schedule post in the past. Scheduled time: {post_datetime}, Current time: {now}")
                return False
            
            # Generate content now (so we have it ready)
            logger.info(f"Generating content for scheduled post (topic: {topic or 'random'})...")
            content = self.content_generator.generate_post(topic)
            
            # Create scheduled post entry
            scheduled_post = {
                'id': f"post_{int(post_datetime.timestamp())}",
                'scheduled_time': post_datetime.isoformat(),
                'topic': topic,
                'content': content,
                'created_at': now.isoformat(),
                'status': 'pending'
            }
            
            # Load existing scheduled posts
            scheduled_posts = self._load_scheduled_posts()
            
            # Add new scheduled post
            scheduled_posts.append(scheduled_post)
            
            # Save to file
            self._save_scheduled_posts(scheduled_posts)
            
            logger.info(f"Post scheduled for {post_datetime.strftime('%Y-%m-%d %H:%M:%S')} {Config.TIMEZONE}")
            logger.info(f"Scheduled post ID: {scheduled_post['id']}")
            
            # Log the next scheduled post
            self._log_next_scheduled_post()
            
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling post: {e}")
            return False
    
    def _check_and_execute_scheduled_posts(self):
        """Check for scheduled posts that are due and execute them"""
        scheduled_posts = self._load_scheduled_posts()
        if not scheduled_posts:
            return
        
        now = datetime.now(Config.get_timezone())
        updated = False
        
        for post in scheduled_posts:
            if post.get('status') != 'pending':
                continue
                
            try:
                scheduled_time = datetime.fromisoformat(post['scheduled_time'])
                # Execute if scheduled time has passed (within 1 minute tolerance)
                if scheduled_time <= now + timedelta(minutes=1):
                    logger.info(f"Executing scheduled post: {post['id']}")
                    
                    # Post the pre-generated content
                    try:
                        result = self.linkedin_api.create_text_post(post['content'])
                        if result:
                            logger.info(f"Scheduled post {post['id']} posted successfully!")
                            logger.info(f"Post ID: {result.get('id', 'Unknown')}")
                            post['status'] = 'completed'
                            post['posted_at'] = now.isoformat()
                            post['linkedin_post_id'] = result.get('id')
                        else:
                            logger.error(f"Failed to post scheduled post {post['id']}")
                            post['status'] = 'failed'
                    except Exception as e:
                        logger.error(f"Error posting scheduled post {post['id']}: {e}")
                        post['status'] = 'failed'
                        post['error'] = str(e)
                    
                    updated = True
            except (ValueError, KeyError) as e:
                logger.warning(f"Invalid scheduled post entry: {e}")
                post['status'] = 'failed'
                post['error'] = str(e)
                updated = True
        
        # Save updated posts
        if updated:
            self._save_scheduled_posts(scheduled_posts)
            # Log the next scheduled post after execution
            self._log_next_scheduled_post()
    
    def get_scheduled_posts(self) -> List[Dict]:
        """Get all scheduled posts"""
        posts = self._load_scheduled_posts()
        # Filter to only show pending posts
        return [p for p in posts if p.get('status') == 'pending']
    
    def get_next_scheduled_post(self) -> Optional[Dict]:
        """Get the next scheduled post (earliest pending post)"""
        scheduled_posts = self.get_scheduled_posts()
        if not scheduled_posts:
            return None
        
        # Sort by scheduled_time and return the earliest one
        try:
            sorted_posts = sorted(
                scheduled_posts,
                key=lambda p: datetime.fromisoformat(p.get('scheduled_time', ''))
            )
            return sorted_posts[0] if sorted_posts else None
        except (ValueError, KeyError) as e:
            logger.warning(f"Error sorting scheduled posts: {e}")
            return scheduled_posts[0] if scheduled_posts else None
    
    def _log_next_scheduled_post(self):
        """Log information about the next scheduled post"""
        next_post = self.get_next_scheduled_post()
        if next_post:
            scheduled_time = datetime.fromisoformat(next_post['scheduled_time'])
            topic_info = f" (topic: {next_post.get('topic', 'random')})" if next_post.get('topic') else ""
            logger.info(f"Next scheduled post: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')} {Config.TIMEZONE}{topic_info}")
            logger.info(f"Post ID: {next_post['id']}")
        else:
            logger.info("No scheduled posts found")

def main():
    """Main function to run the bot"""
    try:
        bot = LinkedInBot()
        
        # Test connection first
        if not bot.test_connection():
            logger.error("LinkedIn API connection failed. Please check your credentials.")
            return
        
        # Start the scheduler
        bot.start_scheduler()
        
    except Exception as e:
        logger.error(f"Bot startup failed: {e}")

if __name__ == "__main__":
    main()
