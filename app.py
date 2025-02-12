import streamlit as st
import google.generativeai as genai
from PIL import Image
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import base64
from io import BytesIO

# Set up page config
st.set_page_config(page_title="AI Image Description", page_icon="📷", layout="wide")

# Custom CSS for better readability
st.markdown("""
    <style>
        body {
            font-family: 'Poppins', sans-serif;
        }
        .main-title {
            text-align: center;
            color: #ff4500;
            font-size: 3rem;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            font-size: 1.3rem;
            color: #444;
            margin-bottom: 30px;
        }
        .uploaded-container {
            display: flex;
            justify-content: center;
        }
        .uploaded-image {
            border-radius: 15px;
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.15);
            max-width: 100%;
            margin-top: 15px;
        }
        .stButton > button {
            border-radius: 10px;
            background: linear-gradient(135deg, #ff4500 30%, #ff6347 100%);
            color: white;
            font-size: 1.1rem;
            padding: 12px;
            transition: all 0.3s ease;
            border: none;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #ff6347 30%, #ff4500 100%);
            transform: scale(1.05);
        }
        .description-box {
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            text-align: center;
            color: #222 !important; /* Fix for readability */
            font-size: 1.2rem; /* Slightly larger text */
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📌 Navigation")
st.sidebar.markdown("Upload an image to generate an AI-powered description.")

# Language selection
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Hindi": "hi",
    "Arabic": "ar",
    "Japanese": "ja",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Korean": "ko",
    "Dutch": "nl",
    "Turkish": "tr",
    "Swedish": "sv",
    "Polish": "pl",
    "Indonesian": "id",
    "Greek": "el",
    "Hebrew": "he",
    "Thai": "th",
    "Vietnamese": "vi",
    "Czech": "cs",
    "Danish": "da",
    "Finnish": "fi",
    "Hungarian": "hu",
    "Romanian": "ro",
    "Ukrainian": "uk"
}

selected_language = st.sidebar.selectbox("🌎 Select output language", list(languages.keys()))

# Enable text-to-speech
enable_tts = st.sidebar.checkbox("🔊 Enable Text-to-Speech")

# Main Title
st.markdown("<h1 class='main-title'>AI Image Description</h1>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

# Function to convert image to base64
def get_image_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_base64 = get_image_base64(image)
    st.markdown(f"<div class='uploaded-container'><img src='data:image/png;base64,{img_base64}' class='uploaded-image'/></div>", unsafe_allow_html=True)

    # Generate description
    st.markdown("### ⏳ Generating Description...")
    api_key = "AIzaSyAD83u7mCoItUs8kcDpA0xQ5yyluESCV1E"
    model_name = "gemini-1.5-flash"
    genai.configure(api_key=api_key)
    client = genai.GenerativeModel(model_name=model_name)

    response = client.generate_content(["Describe this image.", image], stream=True)
    response.resolve()
    description = response.text
    translated_description = GoogleTranslator(source='auto', target=languages[selected_language]).translate(description)

    # Display improved description box
    st.markdown(f"""
        <div class="description-box">
            <h3>📝 Image Description ({selected_language})</h3>
            <p>{translated_description}</p>
        </div>
    """, unsafe_allow_html=True)

    # Text-to-Speech
    if enable_tts:
        tts = gTTS(text=translated_description, lang=languages[selected_language])
        tts.save("description.mp3")
        st.audio("description.mp3", format="audio/mp3")
        os.remove("description.mp3")
