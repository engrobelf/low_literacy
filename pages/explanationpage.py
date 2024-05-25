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

        st.write(f"Time spent on {current_page_title}: {page_duration}")
            # Send data to Data Foundry via OOCSI
        data = {
            "page_name": current_page_title,
            "duration_seconds": page_duration.total_seconds(), 
            'participant_ID': st.session_state.participantID
        }
        st.session_state.oocsi.send('Time_XAI', data)

st.session_state.current_page_title = "Explanation Page"
page_start_time = None
record_page_start_time()

with header2:
    st.title("Letter Selection")

with body2:
    st.header("💡Scenario")
    
    st.markdown('''Imagine it’s a quiet afternoon at home. As you sort through today’s mail, you find a thick, blue envelope marked with a government seal. 
                It stands out among the bills and flyers. Feeling a bit anxious about official documents, you carefully open the envelope. Inside, there’s a letter filled with dense text. Take your time to try and understand what the letter says. 
                What information can you gather from it? After you've done your best to read through the text, please answer the questions related to the content. These questions are designed to help us understand how you handle and interpret official communications. ''')
    st.image('https://images.unsplash.com/photo-1566125882500-87e10f726cdc?q=80&w=2874&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', width=800)

    st.header('Explanation experiment')
    st.markdown('''You will have to read two letters from the Dutch government. One letter realated to health whereas the other one is
                a financial letter. Then, you will compare the summarization tool with a baseline (no summarization) and will need to answer
                some questions on the text to see how well/bad you understood it. Do not worry about getting everything correct!
                I you don't have the answer, an 'I don't know' will also be available. 
                Good luck and thanks again for participating!''')
    st.markdown("After answering the question, you will be asked to evaluate the method you have just seen.")
    
    st.subheader('Model')
    st.markdown(''' A GPT4 model was finetune and prompt engineer to provide the most tailored summary possible. Typical lexical metrics were also used to validate the quality of the 
                summary.''')
    
    st.subheader('Letters')

    # st.subheader('Demographic information')
    # st.markdown("Before you start with the study we would like to ask you to first answer these questions")


# with footer2:
#     if st.button("Start the experiment "):
#         if page_start_time:
#             record_page_duration_and_send_explanation()    
#         record_page_start_time()
#         st.session_state.oocsi.send('XAImethods_attentioncheck', {
#             'participant_ID': st.session_state.participantID,
#             'feature_explanation': feature_explanation,
#             })
#         switch_page(st.session_state.pages[st.session_state.nextPage])

url_directory = "https://raw.githubusercontent.com/engrobelf/low_literacy/main/letters"

#letter_path_test = "https://raw.githubusercontent.com/engrobelf/low_literacy/main/letters/Health.pdf"
# Get the list of PDF files in the directory

with footer2:

    if 'first_topic_selected' not in st.session_state:
        input_method = st.radio("Select first topic", ('Health', 'Financial'))
        selected_pdf = None
        if input_method:
            selected_pdf = os.path.join(url_directory, input_method + '.pdf')
            selected_pdf = selected_pdf.replace('\\', '/')
            st.session_state['uploaded_file'] = selected_pdf
            st.session_state['topic'] = input_method
            st.session_state['second topic'] = 'Health' if st.session_state['topic'] == 'Financial' else 'Financial'
            st.session_state['first_topic_selected'] = True
        else:
            st.write("Please select a topic to proceed.")
            
    
    else:
        if st.session_state['topic'] == 'Health':
            input_method = st.radio("Select second topic", ('Health', 'Financial'))
            selected_pdf = None
            if input_method:
                selected_pdf = os.path.join(url_directory, input_method + '.pdf')
                selected_pdf = selected_pdf.replace('\\', '/')
                st.session_state['uploaded_file'] = selected_pdf
                st.session_state['topic'] = input_method
                st.session_state['second_topic'] = 'Health' if st.session_state['topic'] == 'Financial' else 'Financial'
            else:
                st.write("Please select a topic to proceed.")
        else:
            selected_pdf = st.session_state['uploaded_file']
            
    if st.button("Next page") and selected_pdf is not None:
        
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
            switch_page("Baseline")