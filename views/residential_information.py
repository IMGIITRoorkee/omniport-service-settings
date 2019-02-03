from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from omniport.utils.switcher import load_serializer


class ResidentialInformationView(generics.RetrieveUpdateAPIView):
    """
    View for RU operations on residential information
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = load_serializer('kernel', 'ResidentialInformation')

    def get_object(self):
        """
        Return the residential information of the person currently logged in
        :return: the residential information of the person currently logged in
        """

        person = self.request.person
        try:
            return person.residentialinformation
        except AttributeError:
            raise NotFound(
                detail='Associated residential information not found.'
            )
