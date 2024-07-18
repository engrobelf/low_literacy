import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page
from oocsi_source import OOCSI
import datetime
from datetime import datetime
from gtts import gTTS
import base64
import os


header1, header2, header3 = st.columns([1,4,1])
body1, body2, body3 = st.columns([1,50,1])

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
def record_page_start_time():
    global page_start_time
    page_start_time = datetime.now()

# Function to record page duration and send to Data Foundry
def record_page_duration_and_send():
    current_page_title = st.session_state.current_page_title
    if page_start_time:
        page_end_time = datetime.now()
        page_duration = page_end_time - page_start_time
        st.write(f"Tijd besteed aan {current_page_title}: {page_duration}")
        
        # Send data to Data Foundry via OOCSI
        data = {
            "page_name": current_page_title,
            "duration_seconds": page_duration.total_seconds(), 
            'participant_ID': st.session_state.name
        }
        st.session_state.oocsi.send('Time_XAI', data)

st.session_state.current_page_title = "Laatste Pagina"
page_start_time = None
record_page_start_time()

with header2:
    st.title("Evaluatie - Basislijn")
    # st.write("Dit is het laatste deel van dit experiment.")

with body2:
        # Audios
    text = """
Evaluatie
Deze vragen vragen alleen om uw mening over de methode die u zojuist hebt gebruikt (Geen hulpmiddel)

Effectiviteit
1- Ik kon de belangrijkste ideeën van de tekst snel begrijpen
"Helemaal oneens", "Oneens", "Noch eens noch oneens",  "Eens", "Helemaal eens

2- Uit de tekst voelde ik me zeker over het begrijpen van de inhoud van de brieven:
"Helemaal oneens", "Oneens", "Noch eens noch oneens",  "Eens", "Helemaal eens

3- Het proces hielp me de belangrijke informatie uit de brieven te onthouden:
"Helemaal oneens", "Oneens", "Noch eens noch oneens",  "Eens", "Helemaal eens

Efficiëntie
1- Ik kon mijn lezen binnen een redelijke tijd voltooien:
"Helemaal oneens", "Oneens", "Noch eens noch oneens",  "Eens", "Helemaal eens

2- Ik kon de belangrijkste informatie binnen een redelijke tijd begrijpen
"Helemaal oneens", "Oneens", "Noch eens noch oneens",  "Eens", "Helemaal eens

Cognitieve belasting
1- Ik vond dat de hoeveelheid inspanning die nodig was om de algemene tekst te begrijpen redelijk was:
"Helemaal oneens", "Oneens", "Noch eens noch oneens",  "Eens", "Helemaal eens

2- De taal/terminologie die werd gebruikt was erg gemakkelijk:
"Helemaal oneens", "Oneens", "Noch eens noch oneens",  "Eens", "Helemaal eens

3- Ik investeerde een zeer lage mentale inspanning om de inhoud te begrijpen:
"Helemaal oneens", "Oneens", "Noch eens noch oneens",  "Eens", "Helemaal eens

4- De structuur van de tekst was erg duidelijk:
"Helemaal oneens", "Oneens", "Noch eens noch oneens",  "Eens", "Helemaal eens


        """
        # Add a button with a speaker icon
        
    if st.button("🔊",key="button6"):
            text_to_speech(text)
            audio_player("text.mp3")

        # Clean up the mp3 file after use
    if os.path.exists("text.mp3"):
            os.remove("text.mp3")
        # Text to be read aloud

        # Display the text
        #st.write(text)
        
    with st.form("my_form3", clear_on_submit=True):
        st.subheader("Evaluatie")
        st.write("Deze vragen vragen alleen om uw mening over de methode die u zojuist hebt gebruikt (Geen hulpmiddel)")
        st.subheader('Effectiviteit')
        q1 = st.select_slider('**1**- Ik kon de belangrijkste ideeën van de tekst snel begrijpen',
                                    options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens",  "Eens", 
                            "Helemaal eens"])

        q2 = st.select_slider(
        '**2**- Uit de tekst voelde ik me zeker over het begrijpen van de inhoud van de brieven:',
        options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens",  "Eens", 
                            "Helemaal eens"])

        q3 = st.select_slider(
        '**3**- Het proces hielp me de **belangrijke informatie** uit de brieven te onthouden:',
        options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens",  "Eens", 
                            "Helemaal eens"])
        st.subheader('Efficiëntie')
        q4 = st.select_slider(
        '**1**- Ik kon mijn lezen binnen een redelijke tijd voltooien:',
        options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens",  "Eens", 
                            "Helemaal eens"])

        q5 = st.select_slider(
        '**2**- Ik kon de belangrijkste informatie binnen een redelijke tijd begrijpen',
        options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens",  "Eens", 
                            "Helemaal eens"])
        st.subheader('Cognitieve belasting')
        q6 = st.select_slider(
        '**1**- Ik vond dat de hoeveelheid inspanning die nodig was om de algemene tekst te begrijpen redelijk was:',
        options=["Helemaal oneens", "Oneens", "Noch eens noch oneens",
                  "Eens", "Helemaal eens"])

        q7 = st.select_slider(
        '**2**- De taal/terminologie die werd gebruikt was erg gemakkelijk:',
        options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens", "Eens", 
                            "Helemaal eens"])

        q8 = st.select_slider(
        '**3**- Ik investeerde een zeer lage mentale inspanning om de inhoud te begrijpen:',
        options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens", "Eens", 
                            "Helemaal eens"])

        q9 = st.select_slider(
        '**4**- De structuur van de tekst was erg duidelijk:',
        options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens", "Eens", 
                            "Helemaal eens"])
        # Every form must have a submit button.
        submitted = st.form_submit_button("Indienen")
        if submitted:
            if page_start_time:
                record_page_duration_and_send()    
            st.session_state.oocsi.send('Baseline_feedback', {
                'participant_ID': st.session_state.name,
                'topic': st.session_state['topic'],
                'type of method': 'Baseline',
                'q1': q1,
                'q2': q2,
                'q3': q3,
                'q4': q4,
                'q5': q5,
                'q6': q6,
                'q7': q7,
                'q8': q8,
                'q9': q9,
                
                })
            switch_page('Summarization')