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

# st.session_state.current_page_title = "Explanation Page"
page_start_time = None
record_page_start_time()

with header2:
    st.title("Low literacy issues?")

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


with footer2:
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
            switch_page("Baseline")