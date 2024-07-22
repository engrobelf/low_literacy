"""
Dit zijn de metadata en instructies
Auteur: François Leborgne & Guoze

Instructies:
1. Voer pip install streamlit, oocsi, streamlit_extras uit in je python-omgeving
2. Sla dit bestand ergens op je computer op
3. Navigeer in de opdrachtregel naar waar je bestand staat: "cd/...../folder"

4. Om het te draaien: streamlit run app.py 
5. Klik op de link die je krijgt
6. Je moet soms op opnieuw uitvoeren klikken op de website

Om het menu te verbergen: kopieer en plak dit in config.toml
[ui]
hideSidebarNav = true
"""

import os
from datetime import datetime
import streamlit as st
# from gtts import gTTS
import base64
from oocsi_source import OOCSI
from streamlit_extras.switch_page_button import switch_page
from utils import (
    doc_loader,
    summary_prompt_creator,
    doc_to_final_summary,
    transcript_loader
)
from my_prompts import file_map, file_combine
from streamlit_app_utils import (
    check_gpt_4,
    check_key_validity,
    create_temp_file,
    create_chat_model,
    token_limit,
    token_minimum
)
# Constants
find_clusters = False

st.set_page_config(page_title="Onderzoek naar lage geletterdheid", layout="wide")

# Initialize OOCSI
if 'oocsi' not in st.session_state:
    st.session_state.oocsi = OOCSI('', 'oocsi.id.tue.nl')

# Record start time for each page
def record_page_start_time():
    global page_start_time
    page_start_time = datetime.now()

# Record page duration and send data via OOCSI
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
            'participant_ID': st.session_state.participantID
        }
        st.session_state.oocsi.send('Time_XAI', data)

import streamlit as st
from gtts import gTTS
import os
import base64

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



# Audios
text = """
Hallo en bedankt voor het overwegen om deel te nemen aan ons onderzoeksproject aan de Technische Universiteit Eindhoven, waarbij we een innovatieve GPT-4 samenvattingstool evalueren, deelname volledig vrijwillig is, zonder risico's, en gegevens vertrouwelijk worden behandeld.
"""
st.markdown('''
   :rainbow[ Press 🔊 to listen to the text being read aloud] ''')
# Add a button with a speaker icon
if st.button("🔊",key="button1"):
    text_to_speech(text)
    audio_player("text.mp3")

# Clean up the mp3 file after use
if os.path.exists("text.mp3"):
    os.remove("text.mp3")
# Text to be read aloud

# Display the text
#st.write(text)





# Set up page configuration
st.sidebar.markdown('# Gemaakt door: [François en Sichen ](https://github.com/engrobelf?tab=repositories)')
st.sidebar.markdown('# Git link: [Docsummarizer](https://github.com/engrobelf/low_literacy.git)')
st.sidebar.markdown("""<small>Het is altijd een goede gewoonte om te controleren of een website veilig is voordat je je API-sleutel geeft. 
                    Deze site is open source, dus je kunt de code zelf controleren of de streamlit-app lokaal draaien.</small>""", unsafe_allow_html=True)

page_start_time = None
record_page_start_time()

with st.container():
    st.title("🤖AI Doc Assistant")



with st.container():
    st.header('📄 Informatievorm voor deelnemers')

    st.write('''Hallo en bedankt voor het overwegen om deel te nemen aan ons onderzoeksproject aan de Technische Universiteit Eindhoven. Deze studie omvat een innovatieve GPT-4 samenvattingstool, en uw betrokkenheid zou van onschatbare waarde zijn, vooral gezien uw interesse of expertise in dit veld.

Deelname is geheel vrijwillig, zonder fysieke, juridische of economische risico's. U heeft volledige vrijheid om te kiezen welke vragen u beantwoordt en de mogelijkheid om op elk moment te stoppen, zonder negatieve gevolgen. Als u na het lezen over de studie vragen heeft of meer informatie wilt, neem dan contact op met Sichen Guo.''')

    st.subheader('🎯 Doel en voordeel van de studie')
    st.write('''Het doel van dit onderzoeksproject is om deelnemers uit te nodigen om onze ontworpen tool te gebruiken, real-time interactie te ervaren en directe resultaten te ontvangen. We zullen de effectiviteit van deze interacties evalueren door zowel de duur van de gevalideerde betrokkenheid als de algehele gebruikerservaring te meten via vragenlijsten en interviews.''')
    st.write('''Deze studie wordt uitgevoerd door François Leborgne en Sichen Guo, allen Engineering Doctorate (EngD) stagiairs van het programma Designing Human-System Interaction en voor deze studie onder supervisie van Jun Hu van de afdeling Industrial Design.''')

    st.subheader('🧗 Procedure')
    
    # Audios
    text = """
        Tijdens dit project vragen we u om:
        1. Een brief te kiezen om te uploaden 
        2. De inhoud en informatie te kiezen die u uit deze brief kent
        3. De gekozen brief in het nieuw ontworpen samenvattingssysteem te plaatsen 
        4. De actiepunten of hoogtepunten te kiezen die u uit deze brief kent 
        5. Een enquête met 9 vragen in te vullen 
        6. Aan het eind wordt u uitgenodigd voor een semi-gestructureerd interview
        """
        # Add a button with a speaker icon
        
    if st.button("🔊",key="button2"):
            text_to_speech(text)
            audio_player("text.mp3")

        # Clean up the mp3 file after use
    if os.path.exists("text.mp3"):
            os.remove("text.mp3")
        # Text to be read aloud

        # Display the text
        #st.write(text)

    st.markdown('''
            Tijdens dit project vragen we u om:
                
            1. Een brief te kiezen om te uploaden 
            2. De inhoud en informatie te kiezen die u uit deze brief kent
            3. De gekozen brief in het nieuw ontworpen samenvattingssysteem te plaatsen 
            4. De actiepunten of hoogtepunten te kiezen die u uit deze brief kent 
            5. Een enquête met 9 vragen in te vullen 
            6. Aan het eind wordt u uitgenodigd voor een semi-gestructureerd interview
    ''')

    st.subheader('⚠️ Risico\'s')
    st.markdown("De studie brengt geen risico's, nadelige bijwerkingen of ongemak met zich mee.")

    st.subheader("🕙 Duur")
    st.markdown("De instructies, metingen en debriefing zullen ongeveer 30 minuten duren.")

    st.subheader("🧑‍💼 Vrijwillig")
    st.markdown('''Uw deelname is volledig vrijwillig. U kunt weigeren deel te nemen zonder een reden op te geven en u kunt uw deelname op elk moment tijdens de studie stoppen. U kunt ook uw toestemming om uw gegevens te gebruiken onmiddellijk na het voltooien van de studie intrekken. Dit zal geen negatieve gevolgen voor u hebben.''')

    st.subheader("📊 Vertrouwelijkheid en gebruik, opslag en delen van gegevens")

    # Audios
    text = """
    De verzamelde gegevens worden opgeslagen op door de TU/e ondersteunde opslagfaciliteiten.              
                        We zullen ervoor zorgen dat eventuele gepubliceerde onderzoeksresultaten geen vertrouwelijke of identificeerbare informatie over u bevatten, tenzij u hier expliciet mee instemt, bijvoorbeeld als u wilt dat uw naam in publicaties wordt vermeld.
                        Uw persoonlijke gegevens kunnen worden gebruikt voor toekomstig onderzoek, maar alleen als uw gegevens echt nodig zijn, als de erkende ethische normen voor wetenschappelijk onderzoek worden gevolgd, en als de nieuwe onderzoeksdoelen overeenkomen met de huidige onderzoeksdoelen. Als uw persoonlijke gegevens in toekomstig onderzoek worden gebruikt, zullen we alle redelijke stappen ondernemen om u hierover te informeren. U kunt bezwaar maken tegen het gebruik van uw gegevens voor nieuw onderzoek.                    We kunnen geanonimiseerde gegevens gebruiken voor nieuwe doeleinden zoals onderzoek of onderwijs. We zullen ervoor zorgen dat de gegevens niet aan u kunnen worden gekoppeld en we zullen niets bekendmaken dat u identificeerbaar maakt.
                        Dit onderzoek is beoordeeld en goedgekeurd door de ethische commissie van de Technische Universiteit Eindhoven.
                        Het scherm en de tijd zullen worden opgenomen tijdens het interactieproces, en het interviewscript zal worden opgenomen door middel van audio-opname.
    """
    
    # Add a button with a speaker icon
    if st.button("🔊",key="button4"):
        text_to_speech(text)
        audio_player("text.mp3")

    # Clean up the mp3 file after use
    if os.path.exists("text.mp3"):
        os.remove("text.mp3")
    # Text to be read aloud

    # Display the text
    #st.write(text)

    st.markdown('''De verzamelde gegevens worden opgeslagen op door de TU/e ondersteunde opslagfaciliteiten.              
                    We zullen ervoor zorgen dat eventuele gepubliceerde onderzoeksresultaten geen vertrouwelijke of identificeerbare informatie over u bevatten, tenzij u hier expliciet mee instemt, bijvoorbeeld als u wilt dat uw naam in publicaties wordt vermeld.
                    Uw persoonlijke gegevens kunnen worden gebruikt voor toekomstig onderzoek, maar alleen als uw gegevens echt nodig zijn, als de erkende ethische normen voor wetenschappelijk onderzoek worden gevolgd, en als de nieuwe onderzoeksdoelen overeenkomen met de huidige onderzoeksdoelen. Als uw persoonlijke gegevens in toekomstig onderzoek worden gebruikt, zullen we alle redelijke stappen ondernemen om u hierover te informeren. U kunt bezwaar maken tegen het gebruik van uw gegevens voor nieuw onderzoek.                    We kunnen geanonimiseerde gegevens gebruiken voor nieuwe doeleinden zoals onderzoek of onderwijs. We zullen ervoor zorgen dat de gegevens niet aan u kunnen worden gekoppeld en we zullen niets bekendmaken dat u identificeerbaar maakt.
                    Dit onderzoek is beoordeeld en goedgekeurd door de ethische commissie van de Technische Universiteit Eindhoven.
                    Het scherm en de tijd zullen worden opgenomen tijdens het interactieproces, en het interviewscript zal worden opgenomen door middel van audio-opname.
    ''')

    st.subheader("📰 Verdere informatie")

        # Audios
    text = """
    Als u meer informatie wilt over deze studie, het onderzoeksontwerp of de resultaten, kunt u contact opnemen met François Leborgne (contact email: f.m.g.leborgne@tue.nl ) of Sichen Guo (contact email: s.guo3@tue.nl). 
    Als u klachten heeft over deze studie, neem dan contact op met de supervisor, Jun Hu (j.hu@tue.nl). U kunt onregelmatigheden met betrekking tot wetenschappelijke integriteit melden bij vertrouwenspersonen van de TU/e.
    """
    
    # Add a button with a speaker icon
    if st.button("🔊",key="button5"):
        text_to_speech(text)
        audio_player("text.mp3")

    # Clean up the mp3 file after use
    if os.path.exists("text.mp3"):
        os.remove("text.mp3")
    # Text to be read aloud

    # Display the text
    #st.write(text)

    st.markdown('''Als u meer informatie wilt over deze studie, het onderzoeksontwerp of de resultaten, kunt u contact opnemen met François Leborgne (contact email: f.m.g.leborgne@tue.nl ) of Sichen Guo (contact email: s.guo3@tue.nl). 
    Als u klachten heeft over deze studie, neem dan contact op met de supervisor, Jun Hu (j.hu@tue.nl). U kunt onregelmatigheden met betrekking tot wetenschappelijke integriteit melden bij vertrouwenspersonen van de TU/e.
    ''')

    st.subheader("📝 Informed consent form")
    
    # Audios
    text = """
    1️⃣ Ik heb voldoende informatie over het onderzoeksproject van het aparte informatieblad. Ik heb het gelezen en ik heb de kans gehad om vragen te stellen, die naar tevredenheid zijn beantwoord.
                    
    2️⃣ Ik neem vrijwillig deel aan dit onderzoeksproject. Er is geen expliciete of impliciete druk om deel te nemen aan dit onderzoeksproject, en ik begrijp dat ik mijn deelname op elk moment kan stoppen zonder uit te leggen waarom. Ik hoef geen enkele vraag te beantwoorden die ik niet wil beantwoorden.
                    
    3️⃣ Ik weet dat mijn persoonlijke gegevens zullen worden verzameld en gebruikt voor het onderzoek, zoals uitgelegd in het informatieblad. '4️⃣ Ik stem ermee in dat mijn antwoorden worden gebruikt voor citaten in de onderzoeksresultaten – zonder mijn naam te vermelden.
        """
        # Add a button with a speaker icon
        
    if st.button("🔊",key="button3"):
            text_to_speech(text)
            audio_player("text.mp3")

        # Clean up the mp3 file after use
    if os.path.exists("text.mp3"):
            os.remove("text.mp3")
        # Text to be read aloud

        # Display the text
        #st.write(text)

    st.markdown('''
    1️⃣ Ik heb voldoende informatie over het onderzoeksproject van het aparte informatieblad. Ik heb het gelezen en ik heb de kans gehad om vragen te stellen, die naar tevredenheid zijn beantwoord.
                    
    2️⃣ Ik neem vrijwillig deel aan dit onderzoeksproject. Er is geen expliciete of impliciete druk om deel te nemen aan dit onderzoeksproject, en ik begrijp dat ik mijn deelname op elk moment kan stoppen zonder uit te leggen waarom. Ik hoef geen enkele vraag te beantwoorden die ik niet wil beantwoorden.
                    
    3️⃣ Ik weet dat mijn persoonlijke gegevens zullen worden verzameld en gebruikt voor het onderzoek, zoals uitgelegd in het informatieblad.

    ''')

    # Consent form
    OSF = st.radio

    st.subheader("✍️ Toestemming")
    agree = st.radio(
        '4️⃣ Ik stem ermee in dat mijn antwoorden worden gebruikt voor citaten in de onderzoeksresultaten – zonder mijn naam te vermelden.',
        ('doe ik', 'doe ik niet'), index=1)

    consent_for_osf = "ja" if OSF == 'doe ik' else 'nee'
    # agree = st.radio(
    #         '5️⃣ Ik stem ermee in dat mijn echte naam wordt vermeld in de citaten zoals beschreven onder 4',
    #         ('doe ik', 'doe ik niet'), index=1)

    # consent_for_osf = "ja" if OSF == 'doe ik' else 'nee'

    st.session_state.pages = ['Baseline_health', 'Baseline_financial', 'Tool_health', 'Tool_Financial']

    if 'name' not in st.session_state:
        st.session_state['name'] = ''

    if not st.session_state.name:
        nameID = nameID = st.text_input("Voer hier uw ProlificID in")
        if nameID.strip():
            st.session_state.name = nameID
        else:
            st.write("De invoer kan niet leeg zijn. Probeer het opnieuw.")

    if agree == "doe ik":
        st.write('Bedankt! Ga verder naar de volgende pagina om het experiment te starten')
        if st.button("Volgende pagina"):
            st.session_state.oocsi.send('Lowl_consent', {
                'participant_ID': st.session_state.name,
                'expert': "ja",
                'consent': 'nee',
                'consentForOSF': consent_for_osf
            })
            switch_page("explanationpage")
    else:
        if st.button("Volgende pagina"):
            st.session_state.oocsi.send('Lowl_consent', {
                'participant_ID': st.session_state.name,
                'expert': "ja",
                'consent': 'nee',
                'consentForOSF': consent_for_osf
            })
            switch_page('noconsent')
