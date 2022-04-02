# import io
import os
import streamlit as st

# Imports the Google Cloud client library
from google.cloud import speech

# set path
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret/secret.json'


def transcribe_file(content, lang):
    lang_code = {
        'English': 'en-US',
        'Japanese': 'ja-JP'
    }
    # Instantiates a client
    client = speech.SpeechClient()
    # with io.open(speech_file, 'rb') as f:
    #     content = f.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        # sample_rate_hertz=16000,
        language_code=lang_code[lang],
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        st.write(result.alternatives[0].transcript)
        # print(f"Transcript: {result.alternatives[0].transcript}", end=' |ci: ')
        # print(f"{result.alternatives[0].confidence:.2f}")  # show confidence


st.title("speech to text application")
st.header("Overview")
st.write("this is an application that uses Google speech-to-text.")
st.write("The supported extension for this app is mp3 & wav. "
         "If you would like to use m4a files, please convert them to mp3 files from the following site. "
         "In this case, please set channels to 1 in the advanced settings.")
st.markdown('<a href="https://online-audio-converter.com">online-audio-converter</a>', unsafe_allow_html=True)


upload_file = st.file_uploader("FILE UPLOAD", type=['mp3', 'wav'])
if upload_file is not None:
    content = upload_file.read()
    st.subheader('file details')
    file_details = {
        'File Name': upload_file.name,
        'File Type': upload_file.type,
        'File Size': upload_file.size
    }
    st.write(file_details)
    st.subheader('play sound file')
    st.audio(content)
    st.subheader('Choose language')
    option = st.selectbox('Choose language',
                          ('English', 'Japanese'))
    st.write('Language of choice: ', option)

    st.subheader('convert')
    if st.button('start'):
        comment = st.empty()
        comment.write('Start conversion')
        transcribe_file(content, lang=option)
        comment.write(' ! DONE ! ')
