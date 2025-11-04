import streamlit as st
import time
import logging
from content_generator import ContentGenerator
from config import Config

# Set up logging for Streamlit app
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Gemini Model Comparison",
    page_icon="🤖",
    layout="wide"
)

# Available Gemini models
AVAILABLE_MODELS = {
    "Gemini 2.5 Pro": "gemini-2.5-pro",
    "Gemini 1.5 Pro": "gemini-1.5-pro",
    "Gemini 1.5 Flash": "gemini-1.5-flash",
    "Gemini Pro": "gemini-pro",
}

# Post templates
POST_TEMPLATES = {
    "Tip": "tip_template",
    "Tutorial": "tutorial_template",
    "Trend Analysis": "trend_analysis_template",
    "Comparison": "comparison_template",
    "Best Practice": "best_practice_template",
    "Troubleshooting": "troubleshooting_template",
    "Random": None
}

def main():
    st.title("🤖 Gemini Model Comparison Tool")
    st.markdown("Compare outputs from different Gemini models for LinkedIn post generation")
    
    # Check API key
    if not Config.GEMINI_API_KEY:
        st.error("⚠️ GEMINI_API_KEY not found. Please set it in your environment variables or .env file.")
        st.stop()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        st.subheader("Select Models to Compare")
        selected_models = []
        for model_label, model_id in AVAILABLE_MODELS.items():
            if st.checkbox(model_label, value=(model_label == "Gemini 2.5 Pro"), key=f"model_{model_id}"):
                selected_models.append((model_label, model_id))
        
        if not selected_models:
            st.warning("Please select at least one model to compare.")
        
        st.divider()
        
        # Topic selection
        st.subheader("Topic Selection")
        topic_option = st.radio(
            "Choose topic:",
            ["Random", "Custom"],
            index=0
        )
        
        custom_topic = None
        if topic_option == "Custom":
            custom_topic = st.text_input("Enter topic:", placeholder="e.g., React.js, TypeScript")
        
        st.divider()
        
        # Template selection
        st.subheader("Post Template")
        selected_template_label = st.selectbox(
            "Select template type:",
            list(POST_TEMPLATES.keys()),
            index=6  # Default to Random
        )
        selected_template = POST_TEMPLATES[selected_template_label]
        
        st.divider()
        
        # Generate button
        generate_button = st.button(
            "🚀 Generate Posts",
            type="primary",
            use_container_width=True
        )
    
    # Main content area
    if generate_button:
        if not selected_models:
            st.error("Please select at least one model to compare.")
            st.stop()
        
        topic = custom_topic if custom_topic else None
        
        # Display topic and template info
        with st.expander("📋 Generation Parameters", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Topic:** {topic if topic else 'Random'}")
            with col2:
                st.write(f"**Template:** {selected_template_label}")
        
        # Generate posts for each selected model
        results = {}
        errors = {}
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_models = len(selected_models)
        
        for idx, (model_label, model_id) in enumerate(selected_models):
            status_text.text(f"Generating with {model_label}... ({idx + 1}/{total_models})")
            progress_bar.progress((idx + 1) / total_models)
            
            try:
                logger.info(f"Streamlit app: Generating post with model '{model_id}' for topic '{topic or 'random'}'")
                generator = ContentGenerator(model_name=model_id)
                post = generator.generate_post(topic=topic, template=selected_template)
                results[model_label] = post
                logger.info(f"Streamlit app: Successfully generated post with model '{model_id}'")
            except Exception as e:
                logger.error(f"Streamlit app: Error generating post with model '{model_id}': {e}")
                errors[model_label] = str(e)
                results[model_label] = None
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        progress_bar.empty()
        status_text.empty()
        
        # Display results
        if results:
            st.header("📊 Comparison Results")
            
            # Create columns for side-by-side comparison
            num_models = len(selected_models)
            cols = st.columns(num_models)
            
            for idx, (model_label, model_id) in enumerate(selected_models):
                with cols[idx]:
                    st.subheader(f"🤖 {model_label}")
                    st.caption(f"Model ID: `{model_id}`")
                    
                    if model_label in errors:
                        st.error(f"❌ Error: {errors[model_label]}")
                    elif results[model_label]:
                        # Display the post
                        st.text_area(
                            "Generated Post:",
                            value=results[model_label],
                            height=300,
                            key=f"output_{model_id}",
                            label_visibility="collapsed"
                        )
                        
                        # Add copy button
                        if st.button(f"📋 Copy", key=f"copy_{model_id}"):
                            st.session_state[f"copied_{model_id}"] = True
                            st.toast(f"Copied {model_label} output!", icon="✅")
                        
                        # Show word count
                        word_count = len(results[model_label].split())
                        st.caption(f"📝 Word count: {word_count}")
                    else:
                        st.warning("No output generated")
            
            # Summary section
            st.divider()
            st.subheader("📈 Summary")
            
            summary_cols = st.columns(3)
            with summary_cols[0]:
                st.metric("Models Compared", len(selected_models))
            with summary_cols[1]:
                successful = sum(1 for r in results.values() if r is not None)
                st.metric("Successful", successful)
            with summary_cols[2]:
                failed = len(errors)
                st.metric("Failed", failed)
            
            if errors:
                with st.expander("⚠️ Errors", expanded=False):
                    for model, error in errors.items():
                        st.error(f"**{model}:** {error}")
    
    else:
        # Show instructions when not generating
        st.info("👈 Use the sidebar to configure your comparison and click 'Generate Posts' to start.")
        
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            1. **Select Models**: Choose one or more Gemini models to compare
            2. **Choose Topic**: Select a random topic or enter a custom one
            3. **Select Template**: Pick a post template type (or random)
            4. **Generate**: Click the generate button to create posts
            5. **Compare**: Review the side-by-side outputs
            
            **Tip**: Use the same topic and template for a fair comparison between models.
            """)
        
        with st.expander("📝 Available Models"):
            for model_label, model_id in AVAILABLE_MODELS.items():
                st.markdown(f"- **{model_label}**: `{model_id}`")
        
        with st.expander("📋 Available Templates"):
            for template_label in POST_TEMPLATES.keys():
                if template_label != "Random":
                    st.markdown(f"- **{template_label}**: {POST_TEMPLATES[template_label]}")

if __name__ == "__main__":
    main()

