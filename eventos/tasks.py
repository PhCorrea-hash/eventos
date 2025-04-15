from celery import shared_task

@shared_task
def diga_ola():
    print("Olá, mundo do Celery!")
    return "Celery está funcionando!"