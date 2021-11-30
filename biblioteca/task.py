from biblioteca.email_notify import SendEmail
from biblioteca.service import LivroService
from celery import Celery


app_celery = Celery(
    "tasks",
    backend="rpc://",
    broker="amqp://admin:admin@rabbitmq:5672/"
)


@app_celery.task
def send_email(email: str) -> None:

    path_file = LivroService().make_file_to_email()
    SendEmail(path_file=str(path_file), receiver_email=str(email)).send_csv()
