import time
from celery import shared_task

@shared_task
def send_welcome_email(username):
    print(f"Начинаю отправку письма для {username}...")
    time.sleep(5)
    print(f"Письмо для {username} успешно отправлено!")
    return 'Done'