from shop.celery import app
from .models import User
from django.core.mail import send_mail


@app.task
def send_beat_email():
	for user in User.objects.all():
		send_mail(
        'Special offer just for you!',
        'Buy products upto 30 percent off',
        'atilla.jae.1997@gmail.com',
        [user.email],
        fail_silently = False,)