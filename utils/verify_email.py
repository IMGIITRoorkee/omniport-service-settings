from rest_framework.exceptions import AuthenticationFailed
from formula_one.models import ContactInformation
from formula_one.utils.verification_token import *
from registration.serializers.user import NewUserSerializer
from registration.utils.create import get_new_person
from kernel.models import Person

def send_email(uid, token, email_body, email_subject, url, email_ids, *args, **kwargs):
    """
    This function sends an email containing encoded user id & token
    :param uid: user id associated with verification token
    :param token: verification token for the user
    :param email_body: body of the email
    :param email_subject: subject of the email
    :param url: url to be included in the email body
    :param email_ids email_id of user
    :return: recovery token created
    """

    url= uid + '/' + token
    email_body = email_body.replace('param', url)

    email_push(
        body_text=email_body,
        subject_text=email_subject,
        has_custom_user_target=True,
        email_ids=email_ids,
        category=None
    )

    return token

def get_contact(user):
    """
    contact_information corresponding to the user
    :param query_set:
    :return:
    """
    return Person.objects.get(user=user).contact_information.get()
