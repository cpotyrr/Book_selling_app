from book_selling.celery_controller import app
from django.contrib.auth.models import User
from django.core import mail

@app.task
def send_superuser_emails(title, body):
    connection = mail.get_connection()
    connection.open()

    mail_addresses = User.objects.filter(is_superuser=True).values('email')
    email = mail.EmailMessage(
        title,
        body,
        'from@example.com',
        mail_addresses,
        connection=connection,
    )
    email.send()

