
import streamlit as st
from uuid import uuid4
from streamlit_extras.switch_page_button import switch_page
import random
import pandas as pd
import datetime
import xgboost as xgb
import copy
from PIL import Image
from datetime import datetime, timedelta
import numpy as np

header1, header2, header3 = st.columns([1,12,1])
body1, body2, body3 =st.columns([1,12,1])
footer1, footer2, footer3 =st.columns([1,12,1])

with header2: 
    st.title("Summarization")

with body2:
    st.header("Overview")
    st.markdown("here it ould be nice to have some sort of explanaiton of the LL problem that is faced by a large number of people ")
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
    

input_method = st.radio("Select input method", ('Upload a document', 'another potential feature '))

if input_method == 'Upload a document':
    uploaded_file = st.file_uploader("Upload a document to summarize, 10k to 100k tokens works best!", type=['txt', 'pdf', 'png', 'jpeg'])
    
api_key = st.text_input("Enter API key here, or contact the author if you don't have one.")
st.markdown('[Author email](mailto:f.m.g.leborgne@tue.nl)')
use_gpt_4 = st.checkbox("Use GPT-4 for the final prompt (STRONGLY recommended, requires GPT-4 API access - progress bar will appear to get stuck as GPT-4 is slow)", value=True)
st.sidebar.markdown('# Made by: [François and Sichen ](https://github.com/engrobelf)')
st.sidebar.markdown('# Git link: [Docsummarizer](https://github.com/engrobelf/low_literacy.git)') 
st.sidebar.markdown("""<small>It's always good practice to verify that a website is safe before giving it your API key. 
                    This site is open source, so you can check the code yourself, or run the streamlit app locally.</small>""", unsafe_allow_html=True)


if st.button('Summarize (click once and wait)'):
    if input_method == 'Upload a document':
        process_summarize_button(uploaded_file, api_key, use_gpt_4, find_clusters)

    else:
        doc = transcript_loader(youtube_url)
        process_summarize_button(doc, api_key, use_gpt_4, find_clusters, file=False)


def process_summarize_button(file_or_transcript, api_key, use_gpt_4, find_clusters, file=True):
    """
    Processes the summarize button, and displays the summary if input and doc size are valid

    :param file_or_transcript: The file uploaded by the user or the transcript from the YouTube URL

    :param api_key: The API key entered by the user

    :param use_gpt_4: Whether to use GPT-4 or not

    :param find_clusters: Whether to find optimal clusters or not, experimental

    :return: None
    """
    if not validate_input(file_or_transcript, api_key, use_gpt_4):
        return

    with st.spinner("Summarizing... please wait..."):
        if file:
            temp_file_path = create_temp_file(file_or_transcript)
            doc = doc_loader(temp_file_path)
            map_prompt = file_map
            combine_prompt = file_combine
        else:
            doc = file_or_transcript
            map_prompt = youtube_map
            combine_prompt = youtube_combine
        llm = create_chat_model(api_key, use_gpt_4)
        initial_prompt_list = summary_prompt_creator(map_prompt, 'text', llm)
        final_prompt_list = summary_prompt_creator(combine_prompt, 'text', llm)

        if not validate_doc_size(doc):
            if file:
                os.unlink(temp_file_path)
            return

        if find_clusters:
            summary = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, api_key, use_gpt_4, find_clusters)

        else:
            summary = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, api_key, use_gpt_4)

        st.markdown(summary, unsafe_allow_html=True)
        if file:
            os.unlink(temp_file_path)


def validate_doc_size(doc):
    """
    Validates the size of the document

    :param doc: doc to validate

    :return: True if the doc is valid, False otherwise
    """
    if not token_limit(doc, 800000):
        st.warning('File or transcript too big!')
        return False

    if not token_minimum(doc, 500):
        st.warning('File or transcript too small!')
        return False
    return True


def validate_input(file_or_transcript, api_key, use_gpt_4):
    """
    Validates the user input, and displays warnings if the input is invalid

    :param file_or_transcript: The file uploaded by the user or the YouTube URL entered by the user

    :param api_key: The API key entered by the user

    :param use_gpt_4: Whether the user wants to use GPT-4

    :return: True if the input is valid, False otherwise
    """
    if file_or_transcript == None:
        st.warning("Please upload a file or enter a YouTube URL.")
        return False

    if not check_key_validity(api_key):
        st.warning('Key not valid or API is down.')
        return False

    if use_gpt_4 and not check_gpt_4(api_key):
        st.warning('Key not valid for GPT-4.')
        return False

    return True

if st.button("Next page"):
                # if page_start_time:
                    # record_page_duration_and_send()
                # record_page_start_time()
                # st.session_state.oocsi.send('XAI_consent', {
                #     'participant_ID': st.session_state.participantID,
                #     'expert': "yes",
                #     'consent': 'yes',
                #     'consentForOSF': consentforOSF
                # })
    switch_page("evaluation")