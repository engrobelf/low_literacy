import tempfile
import streamlit as st
import pytesseract
import requests
import PyPDF2
import pdfplumber
import os
from pathlib import Path
from io import StringIO, BytesIO
import pdfplumber


from langchain_openai import ChatOpenAI

from utils import doc_to_text, token_counter

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from PIL import Image


def image_to_text(image):
    # Use Tesseract OCR to extract text from the image
    text = pytesseract.image_to_string(image)
    return text.encode('utf-8')

def pdf_to_text(pdf_path):
    """
    Convert a PDF file to a string of text using PyPDF2.
    :param pdf_path: Path to the PDF file.
    :return: A string of text extracted from the PDF.
    """
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = StringIO()
            for page in pdf_reader.pages:
                text.write(page.extract_text() or "")
            return text.getvalue()
    except Exception as e:
        print("Failed to extract text from PDF:", str(e))
        return None




def load_pdf_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Assuming we are saving the file temporarily to handle it
        from pathlib import Path
        import tempfile

        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        Path(temp.name).write_bytes(response.content)
        return temp.name
    else:
        raise Exception("Failed to download file")


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

def create_temp_file(url):
    """
    Download a PDF from a URL, convert it to text, and save to a temporary text file.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        temp_pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf').name
        Path(temp_pdf_path).write_bytes(response.content)

        text_content = pdf_to_text(temp_pdf_path)
        if text_content:
            temp_text_path = tempfile.NamedTemporaryFile(delete=False, suffix='.txt').name
            with open(temp_text_path, "w", encoding='utf-8') as text_file:
                text_file.write(text_content)
            os.unlink(temp_pdf_path)  # Clean up the temporary PDF file
            return temp_text_path
        else:
            os.unlink(temp_pdf_path)  # Clean up if text extraction fails
            raise Exception("Failed to extract text from PDF")
    except requests.RequestException as e:
        raise Exception(f"Failed to download or process the PDF: {e}")

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



