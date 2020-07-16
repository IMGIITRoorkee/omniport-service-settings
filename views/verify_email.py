from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from formula_one.serializers.generics.contact_information import ContactInformationSerializer
from omniport.utils.switcher import load_serializer
from omniport.settings.configuration.base import CONFIGURATION
from settings.utils.verify_email import send_email, get_contact
from rest_framework import generics, response, status
from kernel.models import Person
from base_auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class VerifyEmailView(generics.GenericAPIView):
    """
    This view when responding to a GET request, generates email verification token
    and sends mail to the concerned user.
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ContactInformationSerializer

    def get(self, request):
        """
        View to serve GET requests
        :param request: the request this is to be responded to
        :return: the response for request
        """
        site_name = CONFIGURATION.site.nomenclature.verbose_name

        url = 'http://stage.channeli.in/api/settings/verify_email/'
        subject = f'{site_name} Email Verification'
        body = f'To verify you email address, please visit {url}param'
        user = request.user
        contact = get_contact(user)
        send_email(
            uid=urlsafe_base64_encode(force_bytes(user.id)),
            token=default_token_generator.make_token(request.user),
            email_body=body,
            email_subject=subject,
            email_ids=[contact.email_address],
            url=url,
        )
        return response.Response(
            data=f'Email sent successfully to {contact.email_address}',
            status=status.HTTP_200_OK,
        )


class VerifyTokenView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        """
        View to serve POST requests to verify the url token and verify email upon validation
        :param request: the request this is to be responded to
        :return: the response for request
        """
        uidb64 = request.GET.get('uid')
        token = request.GET.get('token')
        user = User.objects.get(id=urlsafe_base64_decode(uidb64))
        if_valid = default_token_generator.check_token(user, token)
        if(if_valid):
            Person.objects.get(user=user).contact_information.update(email_address_verified = True)
            response_data = Person.objects.get(user=user).contact_information.get().email_address_verified
        return response.Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )
