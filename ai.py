import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3
import threading
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv('API_key')  # Replace with your  Key
MODEL = os.getenv('Model')
st.set_page_config(page_title="MEDBOT", layout="centered")
st.title("🤖 MEDBOT - Your AI Health Assistant")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
def speak_text(text):
    def tts_worker():
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)  # Set voice speed
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    threading.Thread(target=tts_worker).start()
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Please speak clearly.")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.warning("😕 Sorry, I couldn’t understand what you said.")
    except sr.RequestError:
        st.error("❌ Could not reach the recognition service.")
    return ""
def get_bot_response(message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": st.session_state.chat_history + [{"role": "user", "content": message}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        reply = response.json()["choices"][0]["message"]["content"]
        return reply.strip()
    except Exception as e:
        return f"❌ Error: {e}"
user_input = st.text_input("💬 Type your message or click '🎤 Speak'", key="user_input")

col1, col2 = st.columns(2)
with col1:
    if st.button("🎤 Speak"):
        voice_text = recognize_speech()
        if voice_text:
            user_input = voice_text

with col2:
    if st.button("🔁 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

if user_input:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Get bot response
    bot_response = get_bot_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    
    # Speak bot response
    speak_text(bot_response)
st.markdown("### 💬 Chat History")
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"**🧑 You:** {message['content']}**")
    else:
        st.markdown(f"**🤖 Bot:** {message['content']}**")