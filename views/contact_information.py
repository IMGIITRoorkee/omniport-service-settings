from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from formula_one.serializers.generics.contact_information import (
    ContactInformationSerializer,
)


class ContactInformationView(generics.RetrieveUpdateAPIView):
    """
    View for RU operations on contact information
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ContactInformationSerializer
    def get_object(self):
        """
        Return the contact information of the person currently logged in
        :return: the contact information of the person currently logged in
        """

        person = self.request.person
        try:
            return person.contact_information.first()
        except AttributeError:
            raise NotFound(
                detail='Associated contact information not found.'
            )
