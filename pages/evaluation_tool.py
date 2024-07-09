import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page
from oocsi_source import OOCSI
import datetime
from datetime import datetime

header1, header2, header3 = st.columns([1,4,1])
body1, body2, body3 = st.columns([1,50,1])

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

st.session_state.current_page_title = "evaluation_tool"
page_start_time = None
record_page_start_time()

with header2:
    st.title("Samenvatting Tool - Evaluatie")
    st.write("Dit is het laatste deel van dit experiment.")

with body2:
    with st.form("my_form3", clear_on_submit=True):
        st.subheader("Evaluatie")
        st.write("Deze vragen vragen alleen om uw mening over de methode die u zojuist hebt gebruikt (Samenvatting of Geen hulpmiddel)")
        st.subheader('Effectiviteit')
        q1 = st.select_slider('**1**- Ik kon de belangrijkste ideeën van de tekst snel begrijpen',
                                    options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens", "Eens", 
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
                            "Noch eens noch oneens","Eens", 
                            "Helemaal eens"])

        q5 = st.select_slider(
        '**2**- Ik kon de belangrijkste informatie binnen een redelijke tijd begrijpen',
        options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens", "Eens", 
                            "Helemaal eens"])
        st.subheader('Cognitieve belasting')
        q6 = st.select_slider(
        '**1**- Ik vond dat de hoeveelheid inspanning die nodig was om de algemene tekst te begrijpen redelijk was:',
        options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens", "Eens", 
                            "Helemaal eens"])

        q7 = st.select_slider(
        '**2**- De taal/terminologie die werd gebruikt was erg gemakkelijk:',
        options=["Helemaal oneens", "Oneens",
                            "Noch eens noch oneens", "Eens", 
                            "Helemaal eens"])

        q8 = st.select_slider(
        '**3**- Ik investeerde een zeer lage mentale inspanning om de inhoud te begrijpen:',
        options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens",  "Eens", 
                            "Helemaal eens"])

        q9 = st.select_slider(
        '**4**- De structuur van de tekst was erg duidelijk:',
        options=["Helemaal oneens", "Oneens", 
                            "Noch eens noch oneens",  "Eens", 
                            "Helemaal eens"])
        # Every form must have a submit button.
        submitted = st.form_submit_button("Indienen")
        if submitted:
            if page_start_time:
                record_page_duration_and_send()    
            st.session_state.oocsi.send('Tool_feedback', {
                'participant_ID': st.session_state.name,
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
            switch_page('thankyou')


    # Execute your app
    # embed streamlit docs in a streamlit app
