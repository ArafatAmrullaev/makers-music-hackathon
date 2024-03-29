from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from .tasks import send_activation_code


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.send_activation_code()
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.is_active = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(max_length=150, unique=True)
    username = models.CharField(max_length=150)
    activation_code = models.CharField(max_length=8, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # @staticmethod
    # def generate_activation_code():
    #     from django.utils.crypto import get_random_string
    #     code = get_random_string(8)
    #     return code 
    # def set_activation_code(self):
    #     code = self.generate_activation_code()
    #     if User.objects.filter(activation_code=code).exists():
    #         self.set_activation_code()
    #     else:
    #         self.activation_code = code
    #         self.save()
    # def send_activation_code(self):
    #     # send_activation_code.delay(self.id)
    #     send_activation_code(self.id)

    def generate_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(length=8, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        self.activation_code = code
        self.save()
    
    def send_activation_code(self):
        from django.core.mail import send_mail
        self.generate_activation_code()
        activation_url = f'https://makerskg-music.herokuapp.com/accounts/activate/{self.activation_code}/'
        message = f'Activate your account, following this link {activation_url}'
        send_mail("Activate account", message, "spotify@gmail.com", [self.email])

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = f"Here is the password reset token: {reset_password_token.key}"

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Spotify"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )