import openai
import random
from typing import List, Dict, Any
from datetime import datetime
from config import Config

class ContentGenerator:
    """Generate engaging frontend technology content for LinkedIn posts"""
    
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Frontend technology topics and trends
        self.frontend_topics = [
            "React.js", "Vue.js", "Angular", "Next.js", "Nuxt.js", "Svelte", "Solid.js",
            "TypeScript", "JavaScript ES6+", "CSS Grid", "Flexbox", "Tailwind CSS",
            "Web Components", "Progressive Web Apps", "WebAssembly", "WebRTC",
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
    
    def generate_post(self, topic: str = None) -> str:
        """Generate a LinkedIn post about frontend technology"""
        if not topic:
            topic = random.choice(self.frontend_topics)
        
        template = random.choice(self.post_templates)
        
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
            print(f"Error generating post: {e}")
            return self._generate_fallback_post(topic)
    
    def _generate_tip_post(self, topic: str) -> str:
        """Generate a quick tip post"""
        prompt = f"""
        Create a LinkedIn post about a useful tip for {topic} developers.
        The post should be:
        - Engaging and professional
        - Include a practical tip or insight
        - Be 2-3 sentences long
        - Include relevant hashtags
        - Start with "💡 Frontend Tip:" or similar
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_tutorial_post(self, topic: str) -> str:
        """Generate a mini-tutorial post"""
        prompt = f"""
        Create a LinkedIn post that shares a quick tutorial or how-to about {topic}.
        The post should be:
        - Educational and actionable
        - Include step-by-step guidance or key concepts
        - Be 3-4 sentences long
        - Include relevant hashtags
        - Start with "🚀 Quick Tutorial:" or similar
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_trend_post(self, topic: str) -> str:
        """Generate a trend analysis post"""
        prompt = f"""
        Create a LinkedIn post analyzing current trends or future outlook for {topic}.
        The post should be:
        - Insightful and forward-thinking
        - Include industry perspective
        - Be 3-4 sentences long
        - Include relevant hashtags
        - Start with "📈 Trend Watch:" or similar
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_comparison_post(self, topic: str) -> str:
        """Generate a comparison post"""
        related_topics = [t for t in self.frontend_topics if t != topic]
        compare_topic = random.choice(related_topics)
        
        prompt = f"""
        Create a LinkedIn post comparing {topic} with {compare_topic}.
        The post should be:
        - Balanced and informative
        - Highlight key differences or use cases
        - Be 3-4 sentences long
        - Include relevant hashtags
        - Start with "⚖️ Comparison:" or similar
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_best_practice_post(self, topic: str) -> str:
        """Generate a best practices post"""
        prompt = f"""
        Create a LinkedIn post sharing best practices for {topic}.
        The post should be:
        - Professional and authoritative
        - Include practical advice
        - Be 3-4 sentences long
        - Include relevant hashtags
        - Start with "✨ Best Practice:" or similar
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_troubleshooting_post(self, topic: str) -> str:
        """Generate a troubleshooting post"""
        prompt = f"""
        Create a LinkedIn post about a common issue developers face with {topic} and how to solve it.
        The post should be:
        - Problem-solving focused
        - Include a solution or workaround
        - Be 3-4 sentences long
        - Include relevant hashtags
        - Start with "🔧 Troubleshooting:" or similar
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_fallback_post(self, topic: str) -> str:
        """Generate a simple fallback post if AI generation fails"""
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
