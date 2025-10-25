import schedule
import time
import logging
from datetime import datetime
from typing import Optional
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
        self.is_running = False
        
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
            logger.info(f"Generating content for topic: {topic or 'random'}")
            content = self.content_generator.generate_post(topic)
            logger.info(f"Generated content: {content[:100]}...")
            
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
        
        logger.info(f"Scheduler started - posts will be made daily at {Config.POST_TIME} {Config.TIMEZONE}")
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
