import google.generativeai as genai
import random
import logging
from typing import List, Dict, Any
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Generate engaging frontend technology content for LinkedIn posts using Gemini"""
    
    def __init__(self, model_name: str = 'gemini-2.5-pro'):
        # Configure Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
        logger.info(f"ContentGenerator initialized with model: {model_name}")
        
        # Frontend technology topics and trends
        self.frontend_topics = [
            "React.js", "Next.js",
            "TypeScript", "JavaScript ES6+", "Flexbox", "Tailwind CSS",
            "Web Components", "WebAssembly", "WebRTC",
            "GraphQL", "REST APIs", "Micro-frontends", "Server-Side Rendering",
            "Static Site Generation", "JAMstack", "Webpack", "Vite", "Parcel",
            "Testing", "Jest", "Cypress", "Playwright", "Accessibility", "Performance",
            "Bundle Optimization", "Code Splitting", "Lazy Loading", "Caching Strategies"
        ]
        
        # Post templates and structures
        self.post_templates = [
            "tip_template",
            "tutorial_template", 
            "trend_analysis_template",
            "comparison_template",
            "best_practice_template",
            "troubleshooting_template"
        ]
    
    def generate_post(self, topic: str = None, template: str = None) -> str:
        """Generate a LinkedIn post about frontend technology using Gemini"""
        if not topic:
            topic = random.choice(self.frontend_topics)
        
        if not template:
            template = random.choice(self.post_templates)
        
        logger.info(f"Generating post with model '{self.model_name}' for topic '{topic}' using template '{template}'")
        
        try:
            if template == "tip_template":
                return self._generate_tip_post(topic)
            elif template == "tutorial_template":
                return self._generate_tutorial_post(topic)
            elif template == "trend_analysis_template":
                return self._generate_trend_post(topic)
            elif template == "comparison_template":
                return self._generate_comparison_post(topic)
            elif template == "best_practice_template":
                return self._generate_best_practice_post(topic)
            elif template == "troubleshooting_template":
                return self._generate_troubleshooting_post(topic)
        except Exception as e:
            logger.error(f"Error generating post with Gemini model '{self.model_name}': {e}")
            print(f"Error generating post with Gemini ({self.model_name}): {e}")
            return self._generate_fallback_post(topic)
    
    def _generate_tip_post(self, topic: str) -> str:
        """Generate a quick tip post using Gemini"""
        prompt = f"""
        Create a SINGLE LinkedIn post about a useful tip for {topic} developers.
        The post should be:
        - Engaging and professional
        - Include a practical tip or insight
        - Be 2-3 sentences long
        - Include relevant hashtags
        - Start with "💡 Frontend Tip:" or similar
        Return ONLY ONE post, not multiple options.
        """
        
        try:
            logger.debug(f"Calling Gemini API (model: {self.model_name}) for tip post")
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            logger.info(f"Successfully generated tip post using model '{self.model_name}'")
            return result
        except Exception as e:
            logger.error(f"Gemini API error (model: {self.model_name}): {e}")
            print(f"Gemini API error: {e}")
            return self._generate_fallback_post(topic)
    
    def _generate_tutorial_post(self, topic: str) -> str:
        """Generate a mini-tutorial post using Gemini"""
        prompt = f"""
        Create a SINGLE LinkedIn post that shares a quick tutorial or how-to about {topic}.
        The post should be:
        - Educational and actionable
        - Include step-by-step guidance or key concepts
        - Be 3-4 sentences long
        - Include relevant hashtags
        - Start with "🚀 Quick Tutorial:" or similar
        Return ONLY ONE post, not multiple options.
        """
        
        try:
            logger.debug(f"Calling Gemini API (model: {self.model_name}) for tutorial post")
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            logger.info(f"Successfully generated tutorial post using model '{self.model_name}'")
            return result
        except Exception as e:
            logger.error(f"Gemini API error (model: {self.model_name}): {e}")
            print(f"Gemini API error: {e}")
            return self._generate_fallback_post(topic)
    
    def _generate_trend_post(self, topic: str) -> str:
        """Generate a trend analysis post using Gemini"""
        prompt = f"""
        Create a SINGLE LinkedIn post analyzing current trends or future outlook for {topic}.
        The post should be:
        - Insightful and forward-thinking
        - Include industry perspective
        - Be 3-4 sentences long
        - Include relevant hashtags
        - Start with "📈 Trend Watch:" or similar
        Return ONLY ONE post, not multiple options.
        """
        
        try:
            logger.debug(f"Calling Gemini API (model: {self.model_name}) for trend post")
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            logger.info(f"Successfully generated trend post using model '{self.model_name}'")
            return result
        except Exception as e:
            logger.error(f"Gemini API error (model: {self.model_name}): {e}")
            print(f"Gemini API error: {e}")
            return self._generate_fallback_post(topic)
    
    def _generate_comparison_post(self, topic: str) -> str:
        """Generate a comparison post using Gemini"""
        related_topics = [t for t in self.frontend_topics if t != topic]
        compare_topic = random.choice(related_topics)
        
        prompt = f"""
        Create a SINGLE LinkedIn post comparing {topic} with {compare_topic}.
        The post should be:
        - Balanced and informative
        - Highlight key differences or use cases
        - Be 3-4 sentences long
        - Include relevant hashtags
        - Start with "⚖️ Comparison:" or similar
        Return ONLY ONE post, not multiple options.
        """
        
        try:
            logger.debug(f"Calling Gemini API (model: {self.model_name}) for comparison post")
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            logger.info(f"Successfully generated comparison post using model '{self.model_name}'")
            return result
        except Exception as e:
            logger.error(f"Gemini API error (model: {self.model_name}): {e}")
            print(f"Gemini API error: {e}")
            return self._generate_fallback_post(topic)
    
    def _generate_best_practice_post(self, topic: str) -> str:
        """Generate a best practices post using Gemini"""
        prompt = f"""
        Create a SINGLE LinkedIn post sharing best practices for {topic}.
        The post should be:
        - Professional and authoritative
        - Include practical advice
        - Be 3-4 sentences long
        - Include relevant hashtags
        - Start with "✨ Best Practice:" or similar
        Return ONLY ONE post, not multiple options.
        """
        
        try:
            logger.debug(f"Calling Gemini API (model: {self.model_name}) for best practice post")
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            logger.info(f"Successfully generated best practice post using model '{self.model_name}'")
            return result
        except Exception as e:
            logger.error(f"Gemini API error (model: {self.model_name}): {e}")
            print(f"Gemini API error: {e}")
            return self._generate_fallback_post(topic)
    
    def _generate_troubleshooting_post(self, topic: str) -> str:
        """Generate a troubleshooting post using Gemini"""
        prompt = f"""
        Create a SINGLE LinkedIn post about a common issue developers face with {topic} and how to solve it.
        The post should be:
        - Problem-solving focused
        - Include a solution or workaround
        - Be 3-4 sentences long
        - Include relevant hashtags
        - Start with "🔧 Troubleshooting:" or similar
        Return ONLY ONE post, not multiple options.
        """
        
        try:
            logger.debug(f"Calling Gemini API (model: {self.model_name}) for troubleshooting post")
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            logger.info(f"Successfully generated troubleshooting post using model '{self.model_name}'")
            return result
        except Exception as e:
            logger.error(f"Gemini API error (model: {self.model_name}): {e}")
            print(f"Gemini API error: {e}")
            return self._generate_fallback_post(topic)
    
    def _generate_fallback_post(self, topic: str) -> str:
        """Generate a simple fallback post if Gemini generation fails"""
        tips = [
            f"💡 {topic} tip: Always keep your dependencies updated for better security and performance!",
            f"🚀 Working with {topic}? Remember to optimize your bundle size for faster load times.",
            f"✨ Best practice for {topic}: Write clean, readable code that your future self will thank you for!",
            f"📈 {topic} is evolving rapidly - stay updated with the latest features and best practices!",
            f"🔧 Common {topic} issue? Check your console for errors and use debugging tools effectively."
        ]
        
        return random.choice(tips) + f"\n\n#FrontendDevelopment #{topic.replace('.', '').replace(' ', '')} #WebDevelopment #TechTips"
    
    def get_random_topic(self) -> str:
        """Get a random frontend topic"""
        return random.choice(self.frontend_topics)
    
    def add_hashtags(self, post: str) -> str:
        """Add relevant hashtags to a post if not already present"""
        if "#" not in post:
            hashtags = [
                "#FrontendDevelopment",
                "#WebDevelopment", 
                "#JavaScript",
                "#TechTips",
                "#Programming",
                "#SoftwareDevelopment"
            ]
            return post + "\n\n" + " ".join(hashtags[:3])
        return post