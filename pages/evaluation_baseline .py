import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page
from oocsi_source import OOCSI
import datetime
from datetime import datetime

header1, header2, header3 = st.columns([1,4,1])
body1, body2, body3 =st.columns([1,50,1])

def record_page_start_time():
    global page_start_time
    page_start_time = datetime.now()

# Function to record page duration and send to Data Foundry
def record_page_duration_and_send():
    current_page_title = st.session_state.current_page_title
    if page_start_time:
        page_end_time = datetime.now()
        page_duration = page_end_time - page_start_time
        st.write(f"Time spent on {current_page_title}: {page_duration}")
        
        # Send data to Data Foundry via OOCSI
        data = {
            "page_name": current_page_title,
            "duration_seconds": page_duration.total_seconds(), 
            'participant_ID': st.session_state.name
        }
        st.session_state.oocsi.send('Time_XAI', data)

st.session_state.current_page_title = "Final Page"
page_start_time = None
record_page_start_time()


with header2:
    st.title("Baseline evaluation")
    st.write("This is the final section of baseline evaluation.")


with body2:
    if True:         #st.session_state['topic'] == 'Health':
        with st.form("health_form3", clear_on_submit=True):
            st.subheader("Evaluation")
            st.write("These questions only ask for your opinion about :orange-background[:orange[** the letter you just read**]] ")
            st.subheader('Effectiveness')
            q1 = st.select_slider('**1**- I was able to grasp the main ideas of the text quickly',
                                        options=["Totally disagree", "disagree", 
                                "Neither agree or disagree", "agree", 
                                "Totally agree"])

            q2 = st.select_slider(
            '**2**- From the text, I felt confident understanding the content of the letters:',
            options=["Totally disagree", "disagree",
                                "Neither agree or disagree",  "agree", 
                                "Totally agree"])

            q3 = st.select_slider(
            '**3**- The process helped me retain the **important information** from the letters:',
            options=["Totally disagree", "disagree",
                                "Neither agree or disagree",  "agree", 
                                "Totally agree"])
            st.subheader('Efficiency')
            q4 = st.select_slider(
            '**1**- I was able to complete my reading in a timely manner:',
            options=["Totally disagree", "disagree", 
                                "Neither agree or disagree","agree", 
                                "Totally agree"])

            q5 = st.select_slider(
            '**2**- I was able to understand the key information in a timely manner',
            options=["Totally disagree", "disagree", 
                                "Neither agree or disagree", "agree", 
                                "Totally agree"])
            st.subheader('Cognitive load')
            q6 = st.select_slider(
            '**1**- I felt the amount of effort required to understand the general text was reasonable:',
            options=["Totally disagree", "disagree", 
                                "Neither agree or disagree", "agree", 
                                "Totally agree"])

            q7 = st.select_slider(
            '**2**- The language/ terminology used was very easy:',
            options=["Totally disagree", "disagree",
                                "Neither agree or disagree", "agree", 
                                "Totally agree"])

            q8 = st.select_slider(
            '**3**- I invested a very low mental effort to understand the content:',
            options=["Totally disagree", "disagree", 
                                "Neither agree or disagree",  "agree", 
                                "Totally agree"])

            q9 = st.select_slider(
            '**4**- The structure of the text was very clear:',
            options=["Totally disagree", "disagree", 
                                "Neither agree or disagree",  "agree", 
                                "Totally agree"])
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                if page_start_time:
                    record_page_duration_and_send()    
                # record_page_start_time()
                # st.write("question 1", q1)
                st.session_state.oocsi.send('Baseline_feedback', {
                    'participant_ID': st.session_state.name,
                    'topic': st.session_state['topic'],
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

# Financial Letter questions:
    # elif st.session_state['topic'] == 'Financial':
    #     print(1)
    #     with st.form("financial_form3", clear_on_submit=True):
    #         st.subheader("Evaluation")
    #         st.write("These questions only ask for your opinion about the method you just used  :orange-background[:orange[**Summarization tool**]]")
    #         st.subheader('Effectiveness')
    #         q1 = st.select_slider('**1**- I was able to grasp the main ideas of the text quickly',
    #                                     options=["Totally disagree", "disagree", 
    #                             "Neither agree or disagree", "agree", 
    #                             "Totally agree"])

    #         q2 = st.select_slider(
    #         '**2**- From the text, I felt confident understanding the content of the letters:',
    #         options=["Totally disagree", "disagree",
    #                             "Neither agree or disagree",  "agree", 
    #                             "Totally agree"])

    #         q3 = st.select_slider(
    #         '**3**- The process helped me retain the **important information** from the letters:',
    #         options=["Totally disagree", "disagree",
    #                             "Neither agree or disagree",  "agree", 
    #                             "Totally agree"])
    #         st.subheader('Efficiency')
    #         q4 = st.select_slider(
    #         '**1**- I was able to complete my reading in a timely manner:',
    #         options=["Totally disagree", "disagree", 
    #                             "Neither agree or disagree","agree", 
    #                             "Totally agree"])

    #         q5 = st.select_slider(
    #         '**2**- I was able to understand the key information in a timely manner',
    #         options=["Totally disagree", "disagree", 
    #                             "Neither agree or disagree", "agree", 
    #                             "Totally agree"])
    #         st.subheader('Cognitive load')
    #         q6 = st.select_slider(
    #         '**1**- I felt the amount of effort required to understand the general text was reasonable:',
    #         options=["Totally disagree", "disagree", 
    #                             "Neither agree or disagree", "agree", 
    #                             "Totally agree"])

    #         q7 = st.select_slider(
    #         '**2**- The language/ terminology used was very easy:',
    #         options=["Totally disagree", "disagree",
    #                             "Neither agree or disagree", "agree", 
    #                             "Totally agree"])

    #         q8 = st.select_slider(
    #         '**3**- I invested a very low mental effort to understand the content:',
    #         options=["Totally disagree", "disagree", 
    #                             "Neither agree or disagree",  "agree", 
    #                             "Totally agree"])

    #         q9 = st.select_slider(
    #         '**4**- The structure of the text was very clear:',
    #         options=["Totally disagree", "disagree", 
    #                             "Neither agree or disagree",  "agree", 
    #                             "Totally agree"])
    #         submitted = st.form_submit_button("Submit")
    #         if submitted:
    #             print(2)
    #             st.write("Financial evaluation form submitted with answers:", q1, q2, q3, q4, q5, q6, q7, q8, q9)
    #             if 'page_start_time' in st.session_state:
    #                 record_page_duration_and_send()    
    #             st.session_state.oocsi.send('Baseline_feedback', {
    #             'participant_ID': st.session_state.name,
    #             'topic': st.session_state['topic'],
    #             'type of method': 'Baseline',
    #             'q1': q1,
    #             'q2': q2,
    #             'q3': q3,
    #             'q4': q4,
    #             'q5': q5,
    #             'q6': q6,
    #             'q7': q7,
    #             'q8': q8,
    #             'q9': q9,
                
    #             })
    #         switch_page('Baseline')

            #switch_page('Summarization')





                
    # Execute your app
    # embed streamlit docs in a streamlit app
