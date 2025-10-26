# LinkedIn Frontend Tech Bot 🤖

An automated Python bot that posts daily content about frontend technologies on LinkedIn. The bot generates engaging posts about React, Vue, Angular, TypeScript, CSS, and other frontend technologies using Google's Gemini AI.

## Features ✨

- **Daily Automated Posting**: Posts content every day at a scheduled time
- **AI-Generated Content**: Uses Google Gemini to create engaging frontend tech posts
- **Multiple Post Types**: Tips, tutorials, trend analysis, comparisons, best practices, and troubleshooting
- **LinkedIn API Integration**: Seamless posting to your LinkedIn profile
- **Flexible Scheduling**: Customizable posting time and timezone
- **CLI Interface**: Easy-to-use command line interface
- **Content Variety**: Covers 30+ frontend technologies and frameworks

## Technologies Covered 🚀

- **Frameworks**: React.js, Vue.js, Angular, Next.js, Nuxt.js, Svelte, Solid.js
- **Languages**: TypeScript, JavaScript ES6+, CSS Grid, Flexbox
- **Styling**: Tailwind CSS, CSS-in-JS, Styled Components
- **Tools**: Webpack, Vite, Parcel, Testing frameworks
- **Concepts**: PWAs, Web Components, Micro-frontends, SSR, SSG
- **And many more!**

## Prerequisites 📋

- Python 3.7 or higher
- LinkedIn Developer Account
- Gemini API Key
- LinkedIn App with appropriate permissions

## Installation 🛠️

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run setup**
   ```bash
   python setup.py
   ```

3. **Configure environment**
   - Copy `.env.example` to `.env`
   - Fill in your credentials in the `.env` file

## Configuration ⚙️

### 1. LinkedIn App Setup

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Create a new app
3. Add the following OAuth 2.0 scopes:
   - `r_liteprofile` (Read basic profile)
   - `r_emailaddress` (Read email address)
   - `w_member_social` (Write member social actions)
4. Set redirect URI to: `http://localhost:8080/callback`
5. Note down your Client ID and Client Secret

### 2. Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

### 3. Environment Variables

Create a `.env` file in your project root with the following values:

```env
# LinkedIn API Credentials
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8080/callback
LINKEDIN_ACCESS_TOKEN=your_access_token

# Gemini API Key (AI model for content generation)
GEMINI_API_KEY=your_gemini_api_key

# Bot Configuration - Posts daily at 1:00 AM India Time (IST)
POST_TIME=01:00
TIMEZONE=Asia/Kolkata
```

### 4. Get LinkedIn Access Token

Run the OAuth helper to get your access token:

```bash
python oauth_helper.py
```

This will:
1. Open your browser to LinkedIn authorization
2. Guide you through the OAuth flow
3. Provide you with an access token to add to your `.env` file

## Usage 🚀

### Command Line Interface

The bot provides a comprehensive CLI for different operations:

```bash
# Start the daily posting bot
python cli.py start

# Create and post content immediately
python cli.py post

# Post about a specific topic
python cli.py post --topic "React.js"

# Test LinkedIn API connection
python cli.py test

# Generate content without posting
python cli.py generate

# Generate content for a specific topic
python cli.py generate --topic "TypeScript"

# Show next scheduled post time
python cli.py next

# Enable verbose logging
python cli.py start --verbose
```

### Direct Python Usage

```python
from linkedin_bot import LinkedInBot

# Initialize bot
bot = LinkedInBot()

# Test connection
if bot.test_connection():
    print("LinkedIn API connection successful!")

# Post immediately
success = bot.post_now("React.js")

# Start daily scheduler
bot.start_scheduler()
```

## Post Types 📝

The bot generates different types of posts:

1. **💡 Tips**: Quick, actionable tips for developers
2. **🚀 Tutorials**: Mini-tutorials and how-to guides
3. **📈 Trend Analysis**: Industry insights and future outlook
4. **⚖️ Comparisons**: Technology comparisons and use cases
5. **✨ Best Practices**: Professional advice and standards
6. **🔧 Troubleshooting**: Common issues and solutions

## Scheduling ⏰

- **Default Time**: 1:00 AM IST (India Standard Time) daily
- **Customizable**: Change `POST_TIME` in `.env` file
- **Timezone Support**: Set `TIMEZONE` in `.env` file (e.g., "Asia/Kolkata" for India, "America/New_York" for EST)
- **Format**: 24-hour format (e.g., "01:00" for 1 AM, "14:30" for 2:30 PM)

## Logging 📊

The bot creates detailed logs in:
- Console output (real-time)
- `linkedin_bot.log` file (persistent)

Log levels:
- `INFO`: General operation information
- `ERROR`: Error messages and failures
- `DEBUG`: Detailed debugging information (use `--verbose` flag)

## Troubleshooting 🔧

### Common Issues

1. **LinkedIn API Connection Failed**
   - Verify your access token is valid
   - Check if your LinkedIn app has the correct permissions
   - Ensure your redirect URI matches exactly

2. **Gemini API Errors**
   - Verify your Gemini API key is correct
   - Check your Google AI Studio account
   - Ensure you have API access enabled

3. **Posts Not Appearing**
   - Check LinkedIn's API rate limits
   - Verify your app has `w_member_social` permission
   - Check the logs for specific error messages

### Getting Help

1. Check the logs: `tail -f linkedin_bot.log`
2. Test individual components:
   ```bash
   python cli.py test          # Test LinkedIn API
   python cli.py generate      # Test content generation
   ```
3. Run with verbose logging: `python cli.py start --verbose`

## Customization 🎨

### Adding New Topics

Edit `content_generator.py` and add topics to the `frontend_topics` list:

```python
self.frontend_topics = [
    "React.js", "Vue.js", "Angular",
    "Your New Topic Here",  # Add your topic
    # ... existing topics
]
```

### Custom Post Templates

Create new post templates in `content_generator.py`:

```python
def _generate_custom_post(self, topic: str) -> str:
    prompt = f"""
    Your custom prompt here for {topic}
    """
    # ... implementation
```

### Modifying Post Frequency

Change the scheduling in `linkedin_bot.py`:

```python
# Instead of daily
schedule.every().day.at(Config.POST_TIME).do(self.scheduled_post)

# Use different intervals
schedule.every().monday.at(Config.POST_TIME).do(self.scheduled_post)  # Weekly
schedule.every(6).hours.do(self.scheduled_post)  # Every 6 hours
```

## Cloud Deployment ☁️

### Google Cloud Secret Manager Integration

For production deployments, the bot supports Google Cloud Secret Manager for secure credential management.

**Quick Setup:**

1. Store your secrets in GCP Secret Manager:
   ```bash
   gcloud secrets create linkedin-bot \
     --data-file=env \
     --project=YOUR_PROJECT_ID
   ```

2. Set environment variables:
   ```bash
   export GCP_PROJECT=YOUR_PROJECT_ID
   export USE_SECRET_MANAGER=true
   ```

3. Run your bot - it will automatically fetch secrets from Secret Manager!

**For detailed instructions:**
- 📘 [SECRET_MANAGER_GUIDE.md](SECRET_MANAGER_GUIDE.md) - Complete guide with setup, usage, and troubleshooting
- 📋 [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Step-by-step verification checklist

**Benefits:**
- ✅ Automatic environment detection (Cloud Run, Cloud Functions, etc.)
- ✅ Secure secret storage with access controls
- ✅ Easy secret rotation and versioning
- ✅ Falls back to `.env` for local development

## Security 🔒

- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them regularly
- Use environment variables in production
- **Use Google Cloud Secret Manager for cloud deployments**
- Monitor your LinkedIn app usage and API limits

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License 📄

This project is open source and available under the MIT License.

## Disclaimer ⚠️

This bot is for educational and personal use. Please:
- Follow LinkedIn's Terms of Service
- Respect API rate limits
- Use responsibly and don't spam
- Ensure your content adds value to the community

## Support 💬

If you encounter issues or have questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Open an issue on GitHub
4. Check LinkedIn's API documentation

---

**Happy posting! 🚀**
