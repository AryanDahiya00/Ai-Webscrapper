import streamlit as st
from scrape import (scrape_website, split_dom_content, clean_body_content, extract_body_content)
from parse import parse_with_ollama
import base64

# Add these lines at the beginning of your script
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

# Set page title and layout (must be at the top)
st.set_page_config(page_title="AI Web Scraper", page_icon=":mag:", layout="centered")

# Function to load the local image file and convert it to base64 format
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    # Inject the CSS for setting the background image
    st.markdown(
        f"""
        <style>
        body {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;  /* Cover the entire background */
            background-position: center;  /* Center the image */
            background-repeat: no-repeat;  /* Prevent image repetition */
            height: 100vh;  /* Full viewport height */
            margin: 0;  /* Remove default body margin */
            font-family: 'Times New Roman', Times, serif;  /* Set font to Times New Roman */
        }}
        .stApp {{
            background: transparent;  /* Make the Streamlit app background transparent */
            height: 100vh;  /* Full viewport height for the Streamlit app */
            padding-left: 50px;  /* Add padding to the left */
            margin-left: -500px;  /* Negative margin to shift content further left */
        }}
        h1, h2, h3, h4, h5, h6, p, label {{
            color: white;  /* Adjust the font color to match the background */
        }}
        .stTextInput > div > input {{
            background-color: #222;  /* Darken input background for contrast */
            color: white;
        }}
        .stButton > button {{
            background-color: #444;  /* Dark button background */
            color: white;
        }}
        .parsed-content {{
            color: white;  /* Set the font color of parsed content to white */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to set the background image
set_background("akk.png")  # Replace with the actual filename of your image

# Add title with emoji
st.title("🔍 AI Web Scraper")

# Description
st.markdown("""
    **Welcome to the AI-powered web scraper!** 🚀  
    Easily scrape content from any website and extract relevant information using AI.  
    Just enter a URL, scrape the content, and describe what you want to parse.
""")

# Input URL
st.subheader("🌐 Enter Website URL")
url = st.text_input("Paste the URL of the website you want to scrape:")

# Scrape website button
if st.button("🚀 Scrape Website"):
    if url:
        st.write("🔄 Scraping the website content...")
        result = scrape_website(url)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)

        # Save scraped content in session state
        st.session_state.dom_content = cleaned_content
        
        # Display the DOM content in an expander section
        with st.expander("🔍 View Scraped Content (DOM)"):
            st.text_area("DOM Content", cleaned_content, height=300)
    else:
        st.error("Please enter a valid URL.")

# Parsing section
if "dom_content" in st.session_state:
    st.subheader("📝 Describe What to Parse")
    parse_description = st.text_area("Describe the type of information you want to extract from the content:")

    # Parse content button
    if st.button("🔍 Parse Content"):
        if parse_description:
            st.write("⏳ Parsing content based on your description...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.success("✅ Content parsed successfully!")
            # Display parsed content with white font color
            st.markdown(f"<div class='parsed-content'>{result}</div>", unsafe_allow_html=True)
        else:
            st.error("Please provide a description of what to parse.")