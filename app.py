import streamlit as st
import os
import time
import glob
from gtts import gTTS
from googletrans import Translator

try:
    os.mkdir("temp")
except FileExistsError:
    pass

st.title("Multilingual Text-to-Speech Converter")
st.write("This tool converts text into speech in multiple languages.")

translator = Translator()

text = st.text_input("Enter text")
in_lang = st.selectbox(
    "Select your input language",
    ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"),
)
input_language_dict = {"English": "en", "Hindi": "hi", "Bengali": "bn", "Korean": "ko", "Chinese": "zh-cn", "Japanese": "ja"}
input_language = input_language_dict.get(in_lang, "en")

out_lang = st.selectbox(
    "Select your output language",
    ("English", "Hindi", "Bengali", "Korean", "Chinese", "Japanese"),
)
output_language = input_language_dict.get(out_lang, "en")

def text_to_speech(input_language, output_language, text):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

display_output_text = st.checkbox("Display output text")

if st.button("Convert"):
    result, output_text = text_to_speech(input_language, output_language, text)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Your audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    if display_output_text:
        st.markdown(f"## Output text:")
        st.write(f" {output_text}")

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
