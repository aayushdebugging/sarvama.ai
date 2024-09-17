import streamlit as st
import requests
import base64

# Streamlit app title
st.title("Sarvam.ai Text-to-Speech and Speech-to-Text Demo")

# Input for SARVAM API Key
SARVAM_API_KEY = st.text_input("Enter your SARVAM API Key:", type="password")

# Dropdown for selecting the language
language_options = {
    "Hindi (India)": "hi-IN",
    "English (US)": "en-US",
    "Tamil (India)": "ta-IN",
    "Bengali (India)": "bn-IN"
}
selected_language = st.selectbox("Select Language", list(language_options.keys()))
selected_language_code = language_options[selected_language]

# Divider for separating TTS and STT sections
st.markdown("---")
st.subheader("Text-to-Speech")

# Input text for TTS
input_text = st.text_area("Enter the text for Text-to-Speech:")

if st.button("Convert Text to Speech"):
    # TTS API request
    tts_url = "https://api.sarvam.ai/text-to-speech"
    payload = {
        "inputs": [input_text],
        "target_language_code": selected_language_code,
        "speaker": "meera",  # Change speaker if needed for other languages
        "pitch": 0,
        "pace": 1.65,
        "loudness": 2,
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }
    headers = {"Content-Type": "application/json", "API-Subscription-Key": SARVAM_API_KEY}

    response = requests.post(tts_url, json=payload, headers=headers)

    if response.status_code == 200:
        # Extract audio data from the response
        audio_string = response.text[12:-3]
        audio_data = base64.b64decode(audio_string)

        # Save audio to a file
        with open("output.wav", "wb") as audio_file:
            audio_file.write(audio_data)

        # Play the audio in Streamlit
        st.audio("output.wav", format="audio/wav")
        st.success("Text-to-Speech conversion completed successfully!")
    else:
        st.error("Error in Text-to-Speech conversion.")

# Divider for separating TTS and STT sections
st.markdown("---")
st.subheader("Speech-to-Text")

# File uploader for Speech-to-Text
uploaded_file = st.file_uploader("Upload an audio file for Speech-to-Text", type=["wav", "mp3"])

if uploaded_file is not None and SARVAM_API_KEY:
    # Display uploaded audio
    st.audio(uploaded_file, format="audio/wav")
    
    if st.button("Convert Speech to Text"):
        # Prepare the API request for STT
        stt_url = "https://api.sarvam.ai/speech-to-text"
        files = {
            "file": (uploaded_file.name, uploaded_file, "audio/wav")
        }
        data = {
            "language_code": selected_language_code,
            "model": "saarika:v1"
        }
        headers = {"API-Subscription-Key": SARVAM_API_KEY}
        
        # Make the API request
        response = requests.post(stt_url, data=data, files=files, headers=headers)

        if response.status_code == 200:
            # Display the STT result
            st.write("Speech-to-Text Result:")
            st.json(response.json())
        else:
            st.error("Error in Speech-to-Text conversion.")
else:
    st.info("Please upload an audio file and enter your API key.")
