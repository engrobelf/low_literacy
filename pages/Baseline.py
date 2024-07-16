import streamlit as st
from uuid import uuid4
from streamlit_extras.switch_page_button import switch_page
from utils import calculate_readability_metrics
import random
import pandas as pd
import datetime
import xgboost as xgb
import copy
from PIL import Image
from datetime import datetime, timedelta
from streamlit_app_utils import pdf_to_text, load_pdf_from_github
import numpy as np

import requests
import streamlit as st

header1, header2, header3 = st.columns([1,12,1])
body1, body2, body3 =st.columns([1,12,1])
footer1, footer2, footer3 =st.columns([1,12,1])

# Record page start time function
def record_page_start_time():
    st.session_state['page_start_time'] = datetime.now()

# Record page duration and send data via OOCSI
def record_page_duration_and_send():
    if 'page_start_time' in st.session_state:
        page_duration = datetime.now() - st.session_state['page_start_time']
        st.session_state.oocsi.send('Time_XAI', {
            "page_name": "Baseline - Geen hulpmiddel",
            "duration_seconds": page_duration.total_seconds(),
            "participant_ID": st.session_state.name
        })

record_page_start_time()

with header2: 
    st.title("Baseline - Geen hulpmiddel")

with body2:
    st.header('Uitleg experiment')
    st.markdown('''Lees zorgvuldig de brief met betrekking tot het door jou gekozen veld. Neem de tijd die je nodig hebt en probeer de vragen na de brief te beantwoorden. Bij twijfel, aarzel niet om het antwoord 'Ik weet het niet' te kiezen.''')
    st.subheader('Brief')
        # Assuming the URL is set correctly in your Streamlit app's session state
    pdf_url = st.session_state['uploaded_file']  # Ensure this is set correctly
    pdf_content = load_pdf_from_github(pdf_url)
    if pdf_content:
        text = pdf_to_text(pdf_content)
        if text:
            st.text_area("", text, height=800)  # Display the text in a text area widget
        else:
            st.error("Het is niet gelukt om de PDF naar tekst om te zetten.")
    else:
        st.error("Geen PDF-inhoud om weer te geven.")

    metrics = calculate_readability_metrics(text)
    # st.write("Leesbaarheid Metrieken:")
    # for metric, value in metrics.items():
    #     st.write(f"{metric}: {value}")
    
with body2:
    st.write("Beantwoord alstublieft de volgende vragen:")
    if st.session_state['topic'] == 'Health':
        with st.form("my_form"):
            st.markdown('**Leesbegrip**')
            st.markdown("Selecteer het juiste antwoord op de meerkeuzevragen hieronder. \
                        Een correct antwoord levert +1 punt op, een fout antwoord -1 punt en 'Ik weet het niet' 0 punten.")

            question1 = st.radio(
                "Van welke organisatie is deze brief?",
                ["A) Gezondheidsraad",
                "B) RIVM",
                "C) Ministerie van Volksgezondheid",
                "D) Gemeentehuis",
                "E) Ik weet het niet"], index=4)
            
            question2 = st.radio(
                "Wat is het hoofddoel van deze brief?",
                ["A) Uitnodiging voor een feest",
                "B) Informatie over een coronaprik voor kinderen",
                "C) Advies over schoolbezoeken",
                "D) Registratie voor een sportevenement",
                "E) Ik weet het niet"], index=4)
            
            question3 = st.radio(
                "Welke actie moet als eerste worden ondernomen om een afspraak te maken?",
                ["A) Bel de huisarts",
                "B) Zoek het BSN van je kind",
                "C) Bezoek de lokale kliniek",
                "D) Schrijf je in op een website",
                "E) Ik weet het niet"], index=4)

            question4 = st.radio(
                "Op welk nummer moet je bellen om een vaccinatieafspraak te maken?",
                ["A) 0800 7070",
                "B) 112",
                "C) 0800 1234",
                "D) 30276683",
                "E) Ik weet het niet"], index=4)
            
            question5 = st.radio(
                "Wat is een vereiste om mee te nemen naar de vaccinatieafspraak?",
                ["A) Een waterfles",
                "B) Een pasfoto",
                "C) De uitnodigingsbrief en een ID",
                "D) Een medische geschiedenisrapport",
                "E) Ik weet het niet"], index=4)

            question6 = st.radio(
                "Waar kun je meer informatie vinden over de coronavaccinatie voor kinderen?",
                ["A) www.gezondheid.nl",
                "B) www.rivm.nl",
                "C) www.coronavaccinatie.nl",
                "D) www.kinderzorg.nl",
                "E) Ik weet het niet"], index=4)
            
            submitted = st.form_submit_button("Submit")

            if submitted:
                if 'page_start_time' in st.session_state:
                    record_page_duration_and_send()
                st.session_state.oocsi.send('Baseline_text_question', {
                        'participant_ID': st.session_state.name,
                        'topic': st.session_state['topic'],
                        'q1': question1,
                        'q2': question2,
                        'q3': question3,
                        'q4': question4,
                        'q5': question5,
                        'q6': question6,
                        })
                st.session_state['form_submitted'] = True  

    elif st.session_state['topic'] == 'Financial':
        with st.form("financial_form2"):
            st.markdown('**Reading comprehension**')
            st.markdown("Please select the right answer to the multiple-choice questions below. \
        ")
            question1 = st.radio(
                "Van welke organisatie is deze brief?",
                ["A) Gemeente Amsterdam",
                "B) Gemeente Rotterdam",
                "C) Gemeente Utrecht",
                "D) Gemeente Eindhoven",
                "E) Ik weet het niet"], index=4)

            question2 = st.radio(
                "Wat is het totaalbedrag van de aanslag?",
                ["A) €150,50",
                "B) €200,20",
                "C) €269,72 ",
                "D) €300,30",
                "E) Ik weet het niet"], index=4)

            question3 = st.radio(
                "Wat is de vervaldatum voor de betaling?",
                ["A) 15-02-2024",
                "B) 22-02-2024",
                "C) 31-03-2024",
                "D) 01-04-2024",
                "E) Ik weet het niet"], index=4)

            question4 = st.radio(
                "Hoeveel termijnen kun je kiezen om in te betalen via automatische afschrijving?",
                ["A) 5 termijnen",
                "B) 8 termijnen",
                "C) 10 termijnen",
                "D) 12 termijnen",
                "E) Ik weet het niet"], index=4)

            question5 = st.radio(
                "Waar kun je contact opnemen voor meer informatie of bezwaar maken?",
                ["A) belastingbalie.amsterdam.nl",
                "B) belastingbalie.rotterdam.nl",
                "C) belastingbalie.utrecht.nl",
                "D) belastingbalie.eindhoven.nl",
                "E) Ik weet het niet"], index=4)

            question6 = st.radio(
                "Welke is de juiste contactinformatie?",
                ["A) 14 020",
                "B) 14 040",
                "C) 14 030",
                "D) 14 050",
                "E) Ik weet het niet"], index=4)
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                if 'page_start_time' in st.session_state:
                    record_page_duration_and_send()
                st.session_state.oocsi.send('Baseline_text_question', {
                        'participant_ID': st.session_state.name,
                        'topic': st.session_state['topic'],
                        'q1': question1,
                        'q2': question2,
                        'q3': question3,
                        'q4': question4,
                        'q5': question5,
                        'q6': question6,
                })
                st.session_state['form_submitted'] = True  
        
if 'form_submitted' in st.session_state and st.session_state['form_submitted']:
    st.write("Klik op de knop hieronder om naar de volgende pagina te gaan.")
    if st.button("Volgende pagina"):
        st.session_state['form_submitted'] = False  # 重置提交标记
        print()
        switch_page("evaluation_baseline")
