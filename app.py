import streamlit as st
from google import genai
from google.genai import types
import time

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyB_AX7D5Op6Br-DDv01VVw9Unl4N606HeA")  # 🔑 Replace with your real key

def getGeminiResponse(input_text, length_choice, custom_length, blog_style, tone, keywords, readability, cta, language):
    # Fix the length choice mapping
    if "Short Form" in length_choice:
        no_words = 500
    elif "Medium Form" in length_choice:
        no_words = 1000
    elif "Long Form" in length_choice:
        no_words = 2000
    elif "Custom Length" in length_choice and custom_length:
        try:
            no_words = int(custom_length)
        except (ValueError, TypeError):
            return "⚠️ Please enter a valid number for word count."
    else:
        no_words = 1000

    prompt = f"""
    Write a blog post on the topic "{input_text}".
    - Audience: {blog_style}
    - Tone/Style: {tone}
    - Target Word Count: {no_words}
    - SEO Keywords to include: {keywords}
    - Readability Level: {readability}
    - Call-to-Action: {cta}
    - Language: {language}

    Make it clear, engaging, SEO-optimized, and well-structured with headings.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        if hasattr(response, "text") and response.text:
            return response.text
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return "⚠️ No response generated from Gemini."
    except Exception as e:
        return f"⚠️ Error generating content: {str(e)}"

st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Header Component
st.markdown("""
<div class="header-component">
    <h1 class="main-title">AI-Writer Pro</h1>
    <p class="main-subtitle">Generate premium content with advanced AI technology and custom parameters</p>
</div>
""", unsafe_allow_html=True)

# Main Form Container
st.markdown('<div class="form-container">', unsafe_allow_html=True)

with st.form("blog_form", clear_on_submit=False):
    
    # === CONTENT FOUNDATION SECTION ===
    st.markdown("""
    <div class="section-header">
        <div class="section-icon"></div>
        <div class="section-title">🧩Content Foundation </div>
        
    </div>
    """, unsafe_allow_html=True)
    
    # Primary Input - Full Width
    st.markdown('<div class="primary-input">', unsafe_allow_html=True)
    input_text = st.text_input(
        "Blog Topic & Focus",
        placeholder="e.g., The Revolutionary Impact of AI in Healthcare Diagnostics",
        help="Enter your main topic, title, or key concept"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Two Column Layout
    st.markdown('<div class="two-col-grid">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        keywords = st.text_input(
            "SEO Keywords",
            placeholder="artificial intelligence, healthcare, diagnostics, medical AI",
            help="Comma-separated keywords for search optimization"
        )
    
    with col2:
        cta = st.text_input(
            "Call-to-Action",
            placeholder="Download our healthcare AI guide, Contact our experts",
            help="What action should readers take after reading?"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # === AUDIENCE & STYLE SECTION ===
    st.markdown("""
    <div class="section-header">
        <i class='fas fa-pen' ></i>
        <div class="section-title">Tailor your message</div>
       
    </div>
    """, unsafe_allow_html=True)
    
    # Three Column Layout
    st.markdown('<div class="three-col-grid">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        blog_style_options = [
            "💼 Business Leaders",
            "🔬 Researchers & Academics", 
            "🎓 Students & Learners",
            "⚡ Tech Professionals",
            "🌍 General Public",
            "💡 Industry Experts",
            "🎨 Custom Audience"
        ]
        blog_style = st.selectbox(
            "Target Audience",
            blog_style_options,
            help="Who is your primary reader?"
        )
    
    with col2:
        tone_options = [
            "💼 Professional & Authoritative",
            "💬 Conversational & Friendly", 
            "🎓 Academic & Research-Based",
            "🎯 Persuasive & Compelling",
            "📊 Informative & Educational",
            "📖 Storytelling & Narrative",
            "🎨 Custom Tone"
        ]
        tone = st.selectbox(
            "Writing Style",
            tone_options,
            help="What tone best fits your message?"
        )
    
    with col3:
        readability_options = [
            "🟢 Beginner-Friendly",
            "🟡 Intermediate Level", 
            "🟠 Advanced Technical",
            "🔴 Expert & Specialized",
            "🎨 Custom Level"
        ]
        readability = st.selectbox(
            "Complexity Level",
            readability_options,
            help="How technical should the content be?"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # === FORMAT & DELIVERY SECTION ===
    # st.markdown("""
    # <div class="section-header">
        
       
    #     Structure your content
    # </div>
    # """, unsafe_allow_html=True)

    # Two Column Layout for Length & Language
    st.markdown('<div class="two-col-grid">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])

    with col1:
        length_options = [
            "📑 Short Form (500 words) - Quick reads, social posts",
            "📄 Medium Form (1000 words) - Standard blog posts", 
            "📚 Long Form (2000 words) - In-depth articles",
            "🎛️ Custom Length - You decide"
        ]
        
        length_choice = st.selectbox(
            "Content Length",
            length_options,
            help="Choose the ideal length for your content goals"
        )
        
        # Custom length input with animation
        if "🎛️ Custom Length" in length_choice:
            st.markdown('<div class="custom-input-container show fade-in-scale">', unsafe_allow_html=True)
            custom_length = st.number_input(
                "Specify Word Count",
                min_value=100,
                max_value=5000,
                value=1500,
                step=100,
                help="Enter your desired word count (100-5000 words)",
                key="custom_length_input"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            custom_length = None

    with col2:
        language_options = [
            "🇺🇸 English",
            "🇮🇳 Hindi", 
            "🇪🇸 Spanish",
            "🇫🇷 French",
            "🇩🇪 German",
            "🇮🇹 Italian",
            "🇵🇹 Portuguese",
            "🇷🇺 Russian",
            "🇯🇵 Japanese",
            "🇰🇷 Korean",
            "🇨🇳 Chinese",
            "🇦🇷 Arabic"
        ]
        
        language = st.selectbox(
            "Language",
            language_options,
            help="Choose your content language"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Additional Options
    st.markdown("### Additional Options")
    col5, col6 = st.columns(2)

    with col5:
        include_headings = st.checkbox(
            "📑 Include Section Headings",
            value=True,
            help="Add structured headings to organize content"
        )
        
        include_bullets = st.checkbox(
            "• Include Bullet Points",
            value=False,
            help="Use bullet points for better readability"
        )

    with col6:
        include_cta_checkbox = st.checkbox(
            "📢 Include Call-to-Action",
            value=False,
            help="Add a call-to-action at the end"
        )
        
        include_meta = st.checkbox(
            "🔍 Include SEO Meta Description",
            value=False,
            help="Generate SEO-friendly meta description"
        )

    # Generate Button
    st.markdown('<div class="generate-button">', unsafe_allow_html=True)
    submitted = st.form_submit_button("🚀 Generate Blog Post", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Handle Form Submission
if submitted:
    if not input_text.strip():
        st.error("⚠️ Please enter a blog topic to generate content.")
    else:
        # Show loading spinner
        with st.spinner("🤖 Generating your blog post..."):
            # Call the function to generate content
            result = getGeminiResponse(
                input_text=input_text,
                length_choice=length_choice,
                custom_length=custom_length,
                blog_style=blog_style,
                tone=tone,
                keywords=keywords if keywords else "N/A",
                readability=readability,
                cta=cta if cta else "N/A",
                language=language
            )
            
            # Display the result
            if result and not result.startswith("⚠️"):
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                
                # Result Header
                st.markdown("""
                <div class="result-header">
                    <div class="result-title">✨ Generated Blog Post</div>
                    <div class="result-subtitle">AI-powered content tailored to your specifications</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Result Content
                st.markdown('<div class="result-content">', unsafe_allow_html=True)
                st.write(result)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Action Buttons
                st.markdown("""
                <div class="action-buttons">
                    <p style="color: var(--text-tertiary); font-size: 0.9rem; text-align: center; margin: 0;">
                        📋 Copy the content above or regenerate with different parameters
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Success message
                st.success("🎉 Blog post generated successfully! You can copy the content above.")
                
            else:
                st.error(f"❌ {result}")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem 1rem; color: var(--text-tertiary); font-size: 0.9rem;">
    <p> © 2025 AI-writer All rights reserved | Radhe Radhe 🪷</p>
</div>
""", unsafe_allow_html=True)