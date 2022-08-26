from config.celery import app
from django.core.mail import send_mail

@app.task
def send_activation_code(user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    user = User.objects.get(id=user_id)
    user.generate_activation_code()
    user.set_activation_code()
    activation_url = f'https://makerskg-music.herokuapp.com/account/activate/{user.activation_code}'
    message = f'Activate your account, following this link {activation_url}'
    send_mail("Activate account", message, "change@gmail.com", [user.email])

