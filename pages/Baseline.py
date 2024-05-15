
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
            "page_name": "Baseline - No tool",
            "duration_seconds": page_duration.total_seconds(),
            "participant_ID": st.session_state.name
        })


record_page_start_time()

with header2: 
    st.title("Baseline - No tool")


with body2:
    st.header("Overview")
    st.markdown("explanatio of the task, after clicking the person will need to read the text and try to understand it as much as possible")
    st.image('https://github.com/engrobelf/low_literacy/blob/francois/picture/LL_pic.png?raw=True',  width=700)

    st.header('Explanation experiment')
    st.markdown('''To be modified: In this experiment we will show you four different profiles of passengers. 
    Using Machine Learning (ML) we will show a prediction whether they would have survived the disaster. 
    This prediction is accompanied by each time a different type of explanation.''')
    st.markdown("After seeing four profiles, you will be asked to evaluate the explanation you have just seen.")
    
    st.subheader('Model')
    st.markdown(''' The same ML model is used to generate the predictions of who survived and who did not. 
                This model is used to generate all of the four types of explanations that you will see during the experiment. 
                ''')
    
    st.subheader('Letter')
        # Assuming the URL is set correctly in your Streamlit app's session state
    pdf_url = st.session_state['uploaded_file']  # Ensure this is set correctly
    pdf_content = load_pdf_from_github(pdf_url)
    if pdf_content:
        text = pdf_to_text(pdf_content)
        if text:
            st.text_area("", text, height=800)  # Display the text in a text area widget
        else:
            st.error("Failed to convert PDF to text.")
    else:
        st.error("No PDF content to display.")

    metrics = calculate_readability_metrics(text)
    # st.write("Readability Metrics:")
    # for metric, value in metrics.items():
    #     st.write(f"{metric}: {value}")
    
with body2:
    st.write("Please answer the following questions:")

    with st.form("my_form"):
        st.markdown('**Reading comprehension**')
        st.markdown("Please select the right answer to the multiple-choice questions below. \
                    A correct answer is awarded +1 point, an incorrect answer -1 point and the \"I don't know option\" 0 points.")

        question1 = st.radio(
            "Van welke organisatie is deze brief?",
            ["A) Gezondheidsraad",
            "B) RIVM",
            "C) Ministerie van Volksgezondheid",
            "D) Gemeentehuis",
            "E) I don't know"], index=4)
        
        question2 = st.radio(
            "Wat is het hoofddoel van deze brief?",
            ["A) Uitnodiging voor een feest",
            "B) Informatie over een coronaprik voor kinderen",
            "C) Advies over schoolbezoeken ",
            "D) Registratie voor een sportevenement",
            "E) I don't know"], index=4)
        
        question3 = st.radio(
            "Welke actie moet als eerste worden ondernomen om een afspraak te maken?",
            ["A) Bel de huisarts",
            "B) Zoek het BSN van je kind ",
            "C) Bezoek de lokale kliniek",
            "D) Schrijf je in op een website",
            "E) I don't know"], index=4)

        question4 = st.radio(
            "Op welk nummer moet je bellen om een vaccinatieafspraak te maken?",
            ["A) 0800 7070",
            "B) 112",
            "C) 0800 1234",
            "D) 0900 2020",
            "E) I don't know"], index=4)
        

        question5 = st.radio(
            "Wat is een vereiste om mee te nemen naar de vaccinatieafspraak?",
            ["A) Een waterfles",
            "B) Een pasfoto",
            "C) De uitnodigingsbrief en een ID",
            "D) Een medische geschiedenisrapport",
            "E) I don't know"], index=4)



        question6 = st.radio(
            "Waar kun je meer informatie vinden over de coronavaccinatie voor kinderen?",
            ["A) www.gezondheid.nl",
            "B) www.rivm.nl",
            "C) www.coronavaccinatie.nl",
            "D) www.kinderzorg.nl",
            "E) I don't know"], index=4)
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            if 'page_start_time' in st.session_state:
                record_page_duration_and_send()    
            st.session_state.oocsi.send('Baseline_text_question', {
                'participant_ID': st.session_state.name,
                'q1': question1,
                'q2': question2,
                'q3': question3,
                'q4': question4,
                'q5': question5,
                'q6': question6,
                })

# if submitted: 
if st.button("Next page"):
    switch_page("evaluation_baseline")