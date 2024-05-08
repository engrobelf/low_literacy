# **GPT 3.5/4 Powered Document Summarizer**

## Machine learning courses

Note: Please ensure you have installed <code><a href="https://nodejs.org/en/download/">nodejs</a></code>

Demo it here: https://lowliteracy-bxeunnq5uvyzf2dhunvvf8.streamlit.app/

This is a tool that takes a document (PDF, JPG, JPEG) and generates a concise summary tailored for people with low-literacy using GPT-4 or GPT-3.5-turbo. It can accurately summarize hundreds of pages of text. It's built with Python and Streamlit and leverages the langchain library for text processing.
While the final output is generated with either GPT3.5 or GPT4 (the LLM's that power ChatGPT), only a small portion of the overall document is used in the prompts. Before any call is made to either LLM, the document is separated into
small sections that contain the majority of the meaning of the document.

To preview and run the project on your device:
## Features

- Supports PDF, TXT, and image file formats
- Utilizes GPT-4 or GPT-3.5-turbo for generating summaries
- Automatic clustering of the input document to identify key sections

## Usage

1. Launch the Streamlit app by running `streamlit run main.py`
2. Upload a document to summarize.
3. Enter your OpenAI API key if the free usage cap has been hit.
4. Choose whether to use GPT-4 for the summarization (recommended, requires GPT-4 API access).
5. Click the "Summarize" button and wait for the result.

## Modules

- `main.py`: Streamlit app main file
- `utils.py`: Contains utility functions for document loading, token counting, and summarization
- `streamlit_app_utils.py`: Contains utility functions specifically for the Streamlit app
- `explanationpage.py`: Explanation of the experiment 
- `Baseline.py`: Baseline test - Comprehension question with No summarization tool 
- `Summarization.py`: Comprehension questions with summarization tool
- `evaluation_balesine.py`: Evaluation of the text (baseline - no tool)
- `evaluation_tool.py`: Evaluation of the text (Summaryzation- with tool)

## Main Functions

- `main()`: Entry point for the Streamlit app
- `process_summarize_button()`: Processes the "Summarize" button click and displays the generated summary
- `validate_input()`: Validates user input and displays warnings for invalid inputs
- `validate_doc_size()`: Validates the document size for token limits

## Utility Functions

- `doc_loader()`: Loads a document from a file path
- `token_counter()`: Counts the number of tokens in a text string
- `doc_to_text()`: Converts a langchain Document object to a text string
- `doc_to_final_summary()`: Generates the final summary for a given document
- `load_pdf_from_github()`: Load the pdf tocument from github repo
- `summary_prompt_creator()`: Creates a summary prompt list for the langchain summarize chain
- `pdf_to_text()`: Converts a PDF file to a text string
- `image_to_text()`: Converts a Image file (JPEG, PNG) to a text string
- `check_gpt_4()`: Checks if the user has access to GPT-4
- `token_limit()`: Checks if a document has more tokens than a specified maximum
