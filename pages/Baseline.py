
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
from streamlit_app_utils import pdf_to_text, pdf_url_to_text
import numpy as np

import requests
import streamlit as st
import pdfplumber

header1, header2, header3 = st.columns([1,12,1])
body1, body2, body3 =st.columns([1,12,1])
footer1, footer2, footer3 =st.columns([1,12,1])

# Function to download PDF from URL and convert to text
def pdf_url_to_text(url):
    response = requests.get(url)
    with pdfplumber.open(BytesIO(response.content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


with header2: 
    st.title("Baseline - No tool")

    # URL of the PDF
    pdf_url = "https://github.com/engrobelf/low_literacy/raw/main/letters/Work.pdf"

    # Get text from PDF
    new_text = pdf_url_to_text(st.session_state['uploaded_file'])
    test_text =  pdf_url_to_text(pdf_url)

    # Display text
    st.write(new_text)
    st.write(test_text)

with body2:
    st.header("Overview")
    st.markdown("explanatio of the task, after clicking the person will need to read the text and try to understand it as much as possible")
    st.image('https://github.com/engrobelf/low_literacy/blob/francois/picture/LL_pic.png?raw=True')

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
    new_text = pdf_url_to_text(st.session_state['uploaded_file']).decode('utf-8')
    st.write(new_text)

    metrics = calculate_readability_metrics(new_text)
    st.write("Readability Metrics:")
    for metric, value in metrics.items():
        st.write(f"{metric}: {value}")
    

with body2:
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
            "What is not part of an ANN?",
            ["Input layer",
             "User layer",
             "Output layer",
             "Hidden layer",
             "I don't know"], index=4)
        
        techUser4 = st.radio(
            "Running the same request with the same data on the same AI",
            ["increase the computing speed",
             "never give different results",
             "double the computing time ",
             "could give different results",
             "I don't know"], index=4)
        
        techUser1 = st.radio(
            "What is the central distinction between supervised and unsupervised learning",
            ["Supervised learning uses labelled datasets",
             "Unsupervised learning may happen anytime ",
             "Supervised learning is performed by supervised personnel",
             "Supervised learning supersedes unsupervised learning ",
             "I don't know"], index=4)

        techCreator3 = st.radio(
            "What is not a strictly necessary part of a single AI system's development process?",
            ["Data preprocessing",
             "Model definition",
             "Benchmarking",
             "Training/Learning",
             "I don't know"], index=4)
        

        techUser3 = st.radio(
            "What is a typical application of an AI at which it is usually better than non-AI",
            ["Hardware space analysis",
             "Image recognition ",
             "Creating annual reports",
             "Undefined processes",
             "I don't know"], index=4)



        techCreator1 = st.radio(
            "What always distinguishes decision trees from support vector machine?",
            ["Decision trees are trained faster",
             "Decision trees generate more predictions ",
             "Decision trees are more implicit",
             "Decision trees are more interpretable ",
             "I don't know"], index=4)
        techUser2 = st.radio(
            "Which of the following statements is true?",
            ["Machine Learning is part of AI",
             "Machine Learning and AI are mutually exclusive",
             "AI and ML are the same ",
             "AI is a part of ML",
             "I don't know"], index=4)
        techCreator2 = st.radio(
            "What is a typical split of testing and training data for development purposes?",
            ["80% Training and 20% Testing",
             "40% Training, 40% Testing, 20% Train-Testing together",
             "95% Testing and 5% Training",
             "It does not matter",
             "I don't know"], index=4)
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