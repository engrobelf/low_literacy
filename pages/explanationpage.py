import streamlit as st
from uuid import uuid4
from streamlit_extras.switch_page_button import switch_page
import random
import pandas as pd
import datetime
import xgboost as xgb
import os
import copy
from PIL import Image
from datetime import datetime, timedelta
import numpy as np
from gtts import gTTS
import base64


header1, header2, header3 = st.columns([1,12,1])
body1, body2, body3 =st.columns([1,12,1])
footer1, footer2, footer3 =st.columns([1,12,1])

def record_page_start_time():
    global page_start_time
    page_start_time = datetime.now()

# Function to record page duration and send to Data Foundry
def record_page_duration_and_send_explanation():
    current_page_title = st.session_state.current_page_title
    if page_start_time:
        page_end_time = datetime.now()
        page_duration = page_end_time - page_start_time

        st.write(f"Tijd besteed aan {current_page_title}: {page_duration}")
            # Send data to Data Foundry via OOCSI
        data = {
            "page_name": current_page_title,
            "duration_seconds": page_duration.total_seconds(), 
            'participant_ID': st.session_state.participantID
        }
        st.session_state.oocsi.send('Time_XAI', data)
# Function to convert text to speech and save it as an mp3 file
def text_to_speech(text, lang='nl'):
    tts = gTTS(text=text, lang=lang)
    tts.save("text.mp3")

# Function to embed the audio in the Streamlit app
def audio_player(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f"""
            <audio controls autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            Your browser does not support the audio element.
            </audio>
            """, unsafe_allow_html=True)


st.session_state.current_page_title = "Verklaring Pagina"
page_start_time = None
record_page_start_time()

with header2:
    st.title("Brief Selectie")

with body2:
    st.header("💡Scenario")
    
    # Audios
    text = """
    Stel je voor dat het een rustige middag thuis is. Terwijl je door de post van vandaag sorteert, vind je een dikke, blauwe envelop met een regeringszegel. 
    Het valt op tussen de rekeningen en folders. Een beetje nerveus over officiële documenten, open je voorzichtig de envelop. Binnenin zit een brief vol met dicht opeenstaande tekst. Neem de tijd om te proberen te begrijpen wat de brief zegt. 
    Welke informatie kun je eruit halen? Nadat je je best hebt gedaan om de tekst door te nemen, beantwoord dan de vragen die betrekking hebben op de inhoud. Deze vragen zijn ontworpen om ons te helpen begrijpen hoe je omgaat met en officiële communicatie interpreteert.
        """
        # Add a button with a speaker icon

    if st.button("🔊",key="button4"):
            text_to_speech(text)
            audio_player("text.mp3")

        # Clean up the mp3 file after use
    if os.path.exists("text.mp3"):
            os.remove("text.mp3")
        # Text to be read aloud

        # Display the text
        #st.write(text)

    st.markdown('''Stel je voor dat het een rustige middag thuis is. Terwijl je door de post van vandaag sorteert, vind je een dikke, blauwe envelop met een regeringszegel. 
                Het valt op tussen de rekeningen en folders. Een beetje nerveus over officiële documenten, open je voorzichtig de envelop. Binnenin zit een brief vol met dicht opeenstaande tekst. Neem de tijd om te proberen te begrijpen wat de brief zegt. 
                Welke informatie kun je eruit halen? Nadat je je best hebt gedaan om de tekst door te nemen, beantwoord dan de vragen die betrekking hebben op de inhoud. Deze vragen zijn ontworpen om ons te helpen begrijpen hoe je omgaat met en officiële communicatie interpreteert.''')
    
    st.image('https://images.unsplash.com/photo-1566125882500-87e10f726cdc?q=80&w=2874&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', width=600)


    st.header('Uitleg experiment')

           # Audios
    text = """
    Je moet kiezen tussen 2 verschillende brieven van de Nederlandse overheid met onderwerpen die te maken hebben met belastingen, gezondheid of zelfs een typische controle. 
                Daarna vergelijk je de samenvattingstool met een basislijn (geen samenvatting) en moet je enkele vragen over de tekst beantwoorden om te zien hoe goed (of slecht) 
                je het begrepen hebt. Maak je geen zorgen over het correct krijgen van alles! Als je het antwoord niet weet, is er ook een 'Ik weet het niet' beschikbaar. 
                Veel succes en nogmaals bedankt voor je deelname!
        """
        # Add a button with a speaker icon

    if st.button("🔊",key="button5"):
            text_to_speech(text)
            audio_player("text.mp3")

        # Clean up the mp3 file after use
    if os.path.exists("text.mp3"):
            os.remove("text.mp3")
        # Text to be read aloud

        # Display the text
        #st.write(text)

    st.markdown('''Je moet kiezen tussen 2 verschillende brieven van de Nederlandse overheid met onderwerpen die te maken hebben met belastingen, gezondheid of zelfs een typische controle. 
                Daarna vergelijk je de samenvattingstool met een basislijn (geen samenvatting) en moet je enkele vragen over de tekst beantwoorden om te zien hoe goed (of slecht) 
                je het begrepen hebt. Maak je geen zorgen over het correct krijgen van alles! Als je het antwoord niet weet, is er ook een 'Ik weet het niet' beschikbaar. 
                Veel succes en nogmaals bedankt voor je deelname!''')
    st.markdown("Na het beantwoorden van de vraag wordt u gevraagd de methode te evalueren die u zojuist hebt gezien.")
    
    # st.subheader('Model')
    # st.markdown(''' Een GPT-4-model is fijn afgestemd en prompt-engineered om de meest op maat gemaakte samenvatting mogelijk te maken. Typische lexicale metrics werden ook gebruikt om de kwaliteit van de 
    #             samenvatting te valideren.''')
    
    # st.subheader('Brieven')

    # st.subheader('Demografische informatie')
    # st.markdown("Voordat u met de studie begint, willen we u vragen eerst deze vragen te beantwoorden")

url_directory = "https://raw.githubusercontent.com/engrobelf/low_literacy/main/letters"

# letter_path_test = "https://raw.githubusercontent.com/engrobelf/low_literacy/main/letters/Health.pdf"
# Get the list of PDF files in the directory

input_method = 'Health'
selected_pdf = None
selected_pdf = os.path.join(url_directory, input_method + '.pdf')
selected_pdf = selected_pdf.replace('\\', '/')
st.session_state['uploaded_file'] = selected_pdf
st.session_state['topic'] = input_method
st.session_state['second topic'] = 'Health' if st.session_state['topic'] == 'Financial' else 'Financial'
st.session_state['first_topic_selected'] = True

# with footer2:
#     input_method = st.radio("Selecteer voorkeurs onderwerp", ('Gezondheid', 'Werk', 'Digitale gegevensbescherming', 'Relatie', 'Financieel'))
#     selected_pdf = None
#     if input_method:
#         selected_pdf = os.path.join(url_directory, input_method + '.pdf')
#         selected_pdf = selected_pdf.replace('\\', '/')
#         st.session_state['uploaded_file'] = letter_path_test
#         # st.session_state['uploaded_file'] = selected_pdf
#     else:
#         st.write("Selecteer een onderwerp om verder te gaan.")
          
if st.button("Volgende pagina") and selected_pdf is not None:
                # if page_start_time:
                    # record_page_duration_and_send()
                # record_page_start_time()
                # st.session_state.oocsi.send('XAI_consent', {
                #     'participant_ID': st.session_state.participantID,
                #     'expert': "yes",
                #     'consent': 'yes',
                #     'consentForOSF': consentforOSF
                # })
    if 'selected_pdf' in locals():
        switch_page("baseline")
