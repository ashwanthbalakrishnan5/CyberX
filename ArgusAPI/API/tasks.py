from time import sleep
from celery import shared_task


@shared_task
def test_cel(txt):
    print('txt')
    sleep(15)
    print('done')
