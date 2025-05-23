import requests
from urllib.parse import urljoin, urlparse
from celery import shared_task
from .models import Chatbot, ChatbotCustomization
from django.conf import settings
import os
import requests
from bs4 import BeautifulSoup
import uuid
import re
import secrets
import string
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
import time
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


# llm initialize
llm = ChatGoogleGenerativeAI(
    model=settings.GEMINI_MODEL_NAME,
    google_api_key=settings.GEMINI_API_KEY,
    model_kwargs={"streaming": True})
embedding = HuggingFaceEmbeddings(model_name=settings.EMBEDINGS_MODEL_NAME)

# Prompt initialize
template = """Answer the question using only the context below.
If the context does not contain the answer, just respond with "Unfortunately, I'm not able to answer your query.". Do not explain or expand.

Context:
{context}

Question: {question}
"""
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

def is_reachable_url(web_url):
    """Check given web url is reachable/valid or not"""
    try:
        parsed = urlparse(web_url)
        if not parsed.scheme or not parsed.netloc:
            return False
        response = requests.get(web_url, timeout=5)
        return response.status_code == 200
    except Exception as err:
        print('Website URL checking error:', err)

@shared_task
def process_chatbot(chatbot_id):
    """Start a new task to create a new chat bot"""
    print('***Running process_chatbot***')
    try:
        chatbot = Chatbot.objects.get(id=chatbot_id)

        status = create_chatbot(chatbot.name, chatbot.website_url)
        if status:
            while True:
                api_key = generate_api_key()
                if not Chatbot.objects.filter(api_key=api_key).exists():
                    break

            sdk = f"""<script src="{settings.BASE_URL}/static/js/chatbot.js"
                        data-api-key="{api_key}"></script>"""

            chatbot.api_key = api_key
            chatbot.sdk = sdk
            chatbot.status = 'success'
            chatbot.is_active = True

            ChatbotCustomization.objects.create(chatbot=chatbot)
        else:
            chatbot.status = 'failed'
        chatbot.save()

    except Chatbot.DoesNotExist:
        pass

def get_store_path(store_name):
    """Get vectore store path"""
    return os.path.join(settings.CHROMA_STORE_DIR, store_name)

def text_file(filename, data):
    """Create a text file with given data and return file path"""
    filepath = os.path.join(settings.TEMP_DIR, f'{filename}.txt')
    with open(filepath, 'w') as f:
        f.write(data)
    return filepath

def store_vectors(text_data, store_name):
    """Convert given text_data into emebdings and store in chroma db"""
    textfile = text_file(store_name, text_data)
    loader = TextLoader(textfile)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    persist_directory = get_store_path(store_name)
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        persist_directory=persist_directory
    )
    vectorstore.persist()
    os.remove(textfile)

def load_vectors(store_name):
    """Load vectors from given store name"""
    persist_directory = get_store_path(store_name)
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )
    return vectorstore

def save_to_file(content, filename=False):
    """
    Saves the provided content to a uniquely named text file.

    Args:
        content (str): The text content to save.
        filename (str): Optional filename. If not provided, a unique name is generated.
    """
    if not filename:
        filename = f"{str(uuid.uuid4())[:8]}.txt"

    filepath = os.path.join(settings.TEMP_DIR, filename)
    cleaned_content = re.sub(r'[ \t]+', ' ', content)
    cleaned_content = re.sub(r'\n{3,}', '\n\n', content)
    cleaned_content = re.sub(r' *\n *', '\n', content)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)
    print(f"[Saved] Content written to file: {filepath}")

def is_valid(url, base_netloc):
    """
    Checks if a URL is a valid internal link within the same domain.
    
    Args:
        url (str): URL to validate.
        base_netloc (str): The netloc of the base URL (e.g., 'example.com').

    Returns:
        bool: True if URL is valid and internal, False otherwise.
    """
    parsed = urlparse(url)
    return parsed.scheme in ['http', 'https'] and parsed.netloc == base_netloc

def scrape_url(url, is_main=False):
    """
    Scrapes content from a URL and optionally collects internal links.

    Args:
        url (str): The URL to scrape.
        is_main (bool): If True, also extracts and returns internal links.

    Returns:
        list[str]: List of URLs to process (only when is_main is True).
    """
    print(f"[Fetching] {url}")
    try:
        url = url.rstrip('/')
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove duplicate tags (header, footer, navs)
            if not is_main:
                for tag in soup.find_all(['header', 'footer', 'nav', 'title']):
                    tag.decompose()

            # Save the current page's content
            page_content = soup.get_text().strip()
            filename = f"{url.split('/')[-1]}.txt"
            print(f"[Info] Saving content to {filename}...")
            save_to_file(page_content, filename)

            url_to_process = []

            # If main URL, extract internal links
            if is_main:
                for link_tag in soup.find_all('a', href=True):
                    href = link_tag['href']
                    full_url = urljoin(url, href).rstrip('/')

                    if is_valid(full_url, urlparse(url).netloc) and full_url not in url_to_process and full_url != url:
                        url_to_process.append(full_url)

                print(f"[Info] Found {len(url_to_process)} total links to process.\n")

            return url_to_process if is_main else True

        else:
            print(f"[Error] Failed to retrieve {url} (Status code: {response.status_code})\n")

    except Exception as e:
        print(f"[Exception] Error fetching {url}: {e}\n")

def create_chatbot(bot_name, url):
    """Scrape all the text data from given url and store this data into chroma db"""
    try:
        internal_links = []
        # Start with main page and collect internal links
        internal_links = scrape_url(url, is_main=True)
        
        # Process all collected internal links
        if internal_links:
            for idx, link in enumerate(internal_links, start=1):
                print(f"\n[Processing {idx}/{len(internal_links)}] {link}")
                status = scrape_url(link)
                if status:
                    print(f"[Done] Processed: {link}")
                else:
                    print(f"[Warning] Failed to process: {link}")
                
                time.sleep(1)  # Add delay to avoid overload and rate limits

        # Collect all text files data
        print("Collecting text data from temp files...")
        files = os.listdir(settings.TEMP_DIR)
        content = ""
        for file in files:
            filepath = os.path.join(settings.TEMP_DIR, file)
            with open(filepath, 'r') as f:
                content += f.read() + '\n'
            os.remove(filepath)

        print("Storing vector data...")
        # Store vector data
        store_vectors(content, bot_name)
        print("Vector data stored successfully.")
        return True
    except Exception as err:
        print('Bot creating error:', err)
        return False

def generate_api_key(prefix="cbt_sk_prod", length=24):
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return f"{prefix}_{key}"

def bot_answer(name, question):
    vectors = load_vectors(name)
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectors.as_retriever(),
        chain_type_kwargs={"prompt": prompt, "document_variable_name": "context"},
        return_source_documents=False
    )
    for chunk in chain.stream(question):
        yield chunk

if __name__ == '__main__':
    pass
