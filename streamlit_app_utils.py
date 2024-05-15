import tempfile
import streamlit as st
import pytesseract
import requests
import PyPDF2
import pdfplumber

from io import StringIO, BytesIO

from langchain_openai import ChatOpenAI

from utils import doc_to_text, token_counter

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from PIL import Image


def image_to_text(image):
    # Use Tesseract OCR to extract text from the image
    text = pytesseract.image_to_string(image)
    return text.encode('utf-8')

def pdf_to_text(pdf_content):
    """
    Convert PDF file content (bytes) to a string of text using PyPDF2.

    :param pdf_content: The PDF file content in bytes.
    :return: A string of text.
    """
    try:
        # Convert bytes content to a file-like object
        pdf_file = BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = StringIO()
        for page in pdf_reader.pages:
            text.write(page.extract_text() or "")  # Extract text or use an empty string if none
        return text.getvalue()
    except Exception as e:
        print("Failed to extract text from PDF:", str(e))
        return None


def load_pdf_from_github(url):
    """Fetch PDF content from GitHub."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        st.error("Failed to load PDF from GitHub. Status code: " + str(response.status_code))
        return None


def check_gpt_4(api_key):
    """
    Check if the user has access to GPT-4.

    :param api_key: The user's OpenAI API key.

    :return: True if the user has access to GPT-4, False otherwise.
    """
    try:
        ChatOpenAI(openai_api_key=api_key, model_name='gpt-4').call_as_llm('Hi')
        return True
    except Exception as e:
        return False


def token_limit(doc, maximum=200000):
    """
    Check if a document has more tokens than a specified maximum.

    :param doc: The langchain Document object to check.

    :param maximum: The maximum number of tokens allowed.

    :return: True if the document has less than the maximum number of tokens, False otherwise.
    """
    text = doc_to_text(doc)
    count = token_counter(text)
    print(count)
    if count > maximum:
        return False
    return True


def token_minimum(doc, minimum):
    """
    Check if a document has more tokens than a specified minimum.

    :param doc: The langchain Document object to check.

    :param minimum: The minimum number of tokens allowed.

    :return: True if the document has more than the minimum number of tokens, False otherwise.
    """
    text = doc_to_text(doc)
    count = token_counter(text)
    st.write(count, minimum)
    if count < minimum:
        return False
    return True


def check_key_validity(api_key):
    """
    Check if an OpenAI API key is valid.

    :param api_key: The OpenAI API key to check.

    :return: True if the API key is valid, False otherwise.
    """
    try:
        ChatOpenAI(openai_api_key=api_key).call_as_llm('Hi')
        print('API Key is valid')
        return True
    except Exception as e:
        print('API key is invalid or OpenAI is having issues.')
        print(e)
        return False



def create_temp_file(uploaded_file):
    # Add error handling to check if 'type' attribute exists
    if not hasattr(uploaded_file, 'type'):
        raise AttributeError("Uploaded file is missing the 'type' attribute.")

    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        if uploaded_file.type == 'application/pdf':
            temp_file.write(pdf_to_text(uploaded_file))
        else:
            # Handle other types like images
            pil_image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(pil_image)
            temp_file.write(text.encode('utf-8'))

    return temp_file.name

def create_chat_model(api_key, use_gpt_4):
    """
    Create a chat model ensuring that the token limit of the overall summary is not exceeded - GPT-4 has a higher token limit.

    :param api_key: The OpenAI API key to use for the chat model.

    :param use_gpt_4: Whether to use GPT-4 or not.

    :return: A chat model.
    """
    if use_gpt_4:
        return ChatOpenAI(openai_api_key=api_key, temperature=0, max_tokens=500, model_name='gpt-3.5-turbo')
    else:
        return ChatOpenAI(openai_api_key=api_key, temperature=0, max_tokens=250, model_name='gpt-3.5-turbo')



