import swapper
from rest_framework import generics, response, status, permissions
from rest_framework.exceptions import ValidationError

from base_auth.models import User
from formula_one.serializers.generics.contact_information import \
    ContactInformationSerializer
from formula_one.utils.verification_token import send_token, \
    verify_access_token, delete

from omniport.settings.configuration.base import CONFIGURATION


class VerifyEmailView(generics.GenericAPIView):
    """
    This view when responding to a POST request, generates email verification
    token and sends mail to the concerned user.
    """

    def post(self, request):
        """
        View to serve POST requests
        :param request: the request this is to be responded to
        :return: the response for request
        """

        user = request.user
        person = user.person
        email = request.GET.get('email', None)

        site_name = CONFIGURATION.site.nomenclature.verbose_name
        site_url = CONFIGURATION.allowances.hosts[0]
        token_type = 'VERIFICATION_TOKEN'
        url = f'https://{site_url}/settings/verify_email/?token={token_type}&email={email}'
        subject = f'{site_name} EMAIL VERIFICATION'
        body = f'To verify your {site_name} email address, please visit url'
        if email is None:
            raise ValidationError(detail={'Email address not found'})
        contact = person.contact_information.filter(email_address=email).get()
        if (
                contact is None or
                contact.institute_webmail_address is None
        ):
            return response.Response(
                data=f'Could not fetch email address, '
                     f'please contact the maintainers.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        send_token(
            user_id=user.id,
            person_id=person.id,
            token_type=token_type,
            email_body=body,
            email_subject=subject,
            url=url,
            category=None,
            use_primary_email=False,
            check_if_primary_email_verified=False
        )

        email_id, domain = contact.institute_webmail_address.split('@')
        hidden_email = (f'{email_id[:3]}'
                        f'{"*" * max(len(email_id) - 3, 0)}'
                        f'@{domain}')
        return response.Response(
            data=f'Email sent successfully to {hidden_email}',
            status=status.HTTP_200_OK,
        )


class VerifyTokenView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ContactInformationSerializer

    @verify_access_token
    def get(self, request, *args):
        """
        This view serves GET request, and verifies the email address of the user
        :param request: the request that is being responded to
        :return: the response to the request.
        """

        token_data, verification_token = args[:2]
        email_address = request.GET.get('email')
        print(email_address)
        print(token_data['user_id'])
        print(verification_token)
        user_id = token_data['user_id']
        user = User.objects.get(id=user_id)

        if not user_id or ("VERIFICATION_TOKEN" != token_data['token_type']):
            return response.Response(
                data="Incorrect token type",
                status=status.HTTP_404_NOT_FOUND,
            )

        Person = swapper.load_model('kernel', 'Person')
        try:
            person = Person.objects.get(user=user)
        except Person.DoesNotExist:
            return response.Response(
                data='User corresponding to this token does not exist',
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (not email_address or
                not person.contact_information.first().email_address or
                not person.contact_information.filter(
                    email_address=email_address)
        ):
            return response.Response(
                data="Email address mismatch",
                status=status.HTTP_404_NOT_FOUND,
            )

        Person.objects.get(user=user).contact_information.filter(
            email_address=email_address).update(
            email_address_verified=True)

        delete(verification_token)

        return response.Response(
            data='Successfully verified email.',
            status=status.HTTP_200_OK,
        )
