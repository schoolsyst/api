from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import api_view
from backend.settings import DEBUG
from .models import *
from .serializers import *


class SettingsDefinitionsViewSet(ReadOnlyModelViewSet):
    lookup_field = 'key'
    queryset = SettingDefinition.objects.all()
    serializer_class = SettingDefinitionSerializer


class SettingsViewSet(ModelViewSet):
    lookup_field = 'setting__key'

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return SettingReadSerializer
        return SettingSerializer

    def get_queryset(self):
        return Setting.objects.filter(user__id=self.request.user.id)


class SubjectsViewSet(ModelViewSet):
    lookup_field = 'uuid'
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return Subject.objects.filter(user__pk=self.request.user.id)


class UserViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return UserReadSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.id)


class CurrentUserViewSet(ModelViewSet):
    """
    API endpoint that allows the current user to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCurrentSerializer

    def get_object(self):
        return self.request.user

from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, ReplyTo
from os import environ
from urllib.parse import quote
from datetime import datetime, timedelta

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    # send an e-mail to the user
    expiry_date = datetime.now() + timedelta(hours=24)
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'expiry_date_human': expiry_date.strftime('%A %d %B %Y à %H:%S'), #TODO: french locale
        'reset_password_url':
            "http://localhost:3000/"
            "reset-password/choose"
            f"?token={reset_password_token.key}"
            f"&email={quote(reset_password_token.user.email)}"
    }

    # render email text
    email_html_message = render_to_string('user_reset_password.html', context) # TODO: use https://mjml.io
    email_plaintext_message = render_to_string('user_reset_password.txt', context)

    msg = Mail(
        from_email         = ("passwords@schoolsyst.com", "Schoolsyst"),
        to_emails          = reset_password_token.user.email,
        subject            = "Schoolsyst · Demande de réinitialisation de mot de passe",
        html_content       = email_html_message,
        plain_text_content = email_plaintext_message,
    )
    msg.reply_to           = ReplyTo('ewen.lebihan7@gmail.com', 'Ewen Le Bihan')

    if False:
        print('--------EMAIL--------')
        print(render_to_string('user_reset_password.txt', context))
        print('-------/EMAIL--------')
    else:
        # send w/ sendgrid
        print(f"Getting API key...")
        key = environ.get('SENDGRID_API_KEY')
        if key is None:
            raise Exception("Environment variable SENDGRID_API_KEY not set")
        print(f"Got key: {key}")
        sendgrid = SendGridAPIClient(key)
        print(f"Sending email to {reset_password_token.user.email}...")
        try:
            response = sendgrid.send(msg)
        except Exception as e:
            try:
                print(e.body)
            except AttributeError:
                print(e)
        else:
            print(f"Got {response.status_code} response:")
            print(response.headers)
            print(response.body)

