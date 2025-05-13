import requests
from urllib.parse import urlparse
from celery import shared_task
from .models import Chatbot


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
    try:
        chatbot = Chatbot.objects.get(id=chatbot_id)

        import time
        time.sleep(5)

        chatbot.status = 'success'
        chatbot.save()

    except Chatbot.DoesNotExist:
        pass
