from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import api_view
from backend.settings import DEBUG
from .models import *
from .serializers import *


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

    # get data
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

    # send the mail
    print('Sending mail...')
    send_mail(
        subject="schoolsyst · Demande de réinitialisation de mot de passe",
        message=email_plaintext_message,
        from_email=("schoolsyst", "passwords@schoolsyst.com"),
        recipient_list=[reset_password_token.user.email],
        html_message=email_html_message
    )
