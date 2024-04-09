import streamlit as st
import os
import time
import glob
import os

from gtts import gTTS

# Create a temporary directory if it doesn't exist
try:
    os.mkdir("temp")
except:
    pass

# Title with Emoji
st.title("🔊 Text to Speech 🔊")

# Description of the project
st.write("This is a simple text-to-speech converter that converts English text into speech.")

# Input Text
text = st.text_input("Enter text")

# Select output language
out_lang = st.selectbox(
    "Select your output language",
    ("English",)
)

# Mapping output languages to language codes
language_codes = {"English": "en"}
output_language = language_codes[out_lang]

# Select English accent
english_accent = st.selectbox(
    "Select your English accent",
    (
        "Default",
        "India",
        "United Kingdom",
        "United States",
        "Canada",
        "Australia",
        "Ireland",
        "South Africa",
    ),
)

# Mapping English accents to top-level domains (TLDs) for Google Translate
accent_tlds = {
    "Default": "com",
    "India": "co.in",
    "United Kingdom": "co.uk",
    "United States": "com",
    "Canada": "ca",
    "Australia": "com.au",
    "Ireland": "ie",
    "South Africa": "co.za",
}
tld = accent_tlds[english_accent]

# Function to convert text to speech
def text_to_speech(text, output_language, tld):
    tts = gTTS(text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[:20] if len(text) > 20 else text  # Limiting file name to 20 characters
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name

# Convert button
if st.button("Convert"):
    result = text_to_speech(text, output_language, tld)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Your audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

# Function to remove old files
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

# Remove files older than 7 days
remove_files(7)
