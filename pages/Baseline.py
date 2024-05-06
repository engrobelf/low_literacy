
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

# Function to download PDF from URL and convert to text



with header2: 
    st.title("Baseline - No tool")


with body2:
    st.header("Overview")
    st.markdown("explanation of the task, after clicking the person will need to read the text and try to understand it as much as possible")
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
            st.text_area("PDF Text", text, height=800)  # Display the text in a text area widget
        else:
            st.error("Failed to convert PDF to text.")
    else:
        st.error("No PDF content to display.")

    metrics = calculate_readability_metrics(text)
    st.write("Readability Metrics:")
    for metric, value in metrics.items():
        st.write(f"{metric}: {value}")

if 'selected_topic' in st.session_state:
    if st.session_state['selected_topic'] == 'Health':
        with st.form("health_form"):
        # add queation form related to health
            st.subheader("Questionnaire I for Health")
        # questionnaire
elif st.session_state['selected_topic'] == 'Relationship':
    with st.form("relationship_form"):
        # add queation form related to relationship
        st.subheader("Questionnaire II for Relationship")
        # questionnaire
    
with body2:
    st.subheader("Questionnaire I")
    st.write("Please answer the following questions:")
    # if 'selected_topic' in st.session_state:
        # if st.session_state['selected_topic'] == 'Health':
        #  with st.form("health_form"):
        #     st.write("Please answer the following questions:")
    

    with st.form("my_form"):
        st.markdown('**Reading comprehension**')
        st.markdown("Please select the right answer to the multiple-choice questions below. \
                    A correct answer is awarded +1 point, an incorrect answer -1 point and the \"I don't know option\" 0 points.")

        # socio1 = st.radio(
        # "AI was first mention in",
        # ["The 2000s",
        #  "The 1950s",
        #  "The 1880s",
        #  "The 1980s",
        #  "I don't know"], index =4)

        # socio2 = st.radio(
        # "How are human and artificial intelligence related?",
        # ["They are the same, concerning strengths and weaknesses",
        #  "They predict each other",
        #  "Their strengths and weaknesses converge",
        #  "They are different, each has its own strengths and weaknesses",
        #  "I don't know"], index =4)

        # socio3 = st.radio(
        # "AI research",
        # ["happens in an interdisciplinary field including multiple technologies ",
        #  "refers to one specific AI technology",
        #  "is only fiction at this point in time ",
        #  "revolves predominantly around optimization ",
        #  "I don't know"], index =4)

        # socio4 = st.radio(
        # "What is a possible risk for humans of AI technology",
        # ["Digital assistants take over self-driving cars",
        #  "Voice generators make people unlearn natural languages",
        #  "Image generator break the rule of art ",
        #  "Deep fakes render videos unattributable",
        #  "I don't know"], index =4)
        
        techCreator4 = st.radio(
            "Van welke organisatie is deze brief?",
            ["A) Gezondheidsraad",
            "B) RIVM",
            "C) Ministerie van Volksgezondheid",
            "D) Gemeentehuis",
            "E) I don't know"], index=4)
        
        techUser4 = st.radio(
            "Wat is het hoofddoel van deze brief?",
            ["A) Uitnodiging voor een feest",
            "B) Informatie over een coronaprik voor kinderen",
            "C) Advies over schoolbezoeken ",
            "D) Registratie voor een sportevenement",
            "E) I don't know"], index=4)
        
        techUser1 = st.radio(
            "Welke actie moet als eerste worden ondernomen om een afspraak te maken?",
            ["A) Bel de huisarts",
            "B) Zoek het BSN van je kind ",
            "C) Bezoek de lokale kliniek",
            "D) Schrijf je in op een website",
            "E) I don't know"], index=4)

        techCreator3 = st.radio(
            "Op welk nummer moet je bellen om een vaccinatieafspraak te maken?",
            ["A) 0800 7070",
            "B) 112",
            "C) 0800 1234",
            "D) 0900 2020",
            "E) I don't know"], index=4)
        

        techUser3 = st.radio(
            "Wat is een vereiste om mee te nemen naar de vaccinatieafspraak?",
            ["A) Een waterfles",
            "B) Een pasfoto",
            "C) De uitnodigingsbrief en een ID",
            "D) Een medische geschiedenisrapport",
            "E) I don't know"], index=4)



        techCreator1 = st.radio(
            "Waar kun je meer informatie vinden over de coronavaccinatie voor kinderen?",
            ["A) www.gezondheid.nl",
            "B) www.rivm.nl",
            "C) www.coronavaccinatie.nl",
            "D) www.kinderzorg.nl",
            "E) I don't know"], index=4)
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            pass
            # if page_start_time:
            #     record_page_duration_and_send()    
            # # st.write("question 1", q1)
            # st.session_state.oocsi.send('XAImethods_evaluation', {
            #     'participant_ID': st.session_state.participantID,
            #     'type of explanation': 'Decision tree',
            #     'cognitive load': c_load,
            #     'q1': q1,
            #     'q2': q2,
            #     'q3': q3,
            #     'q4': q4,
            #     'q5': q5,
            #     'q6': q6,
            #     'q7': q7,
            #     'q8': q8,
                
            #     })

# if submitted: 
if st.button("Next page"):
                # if page_start_time:
                    # record_page_duration_and_send()
                # record_page_start_time()
                # st.session_state.oocsi.send('Baseline_text_question', {
                #     'participant_ID': st.session_state.participantID,
                #     'expert': "yes",
                #     'consent': 'yes',
                #     'consentForOSF': consentforOSF
                # })
    switch_page("evaluation_baseline")