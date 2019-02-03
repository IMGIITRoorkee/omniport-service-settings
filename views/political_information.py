from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from omniport.utils.switcher import load_serializer


class PoliticalInformationView(generics.RetrieveUpdateAPIView):
    """
    View for RU operations on political information
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = load_serializer('kernel', 'PoliticalInformation')

    def get_object(self):
        """
        Return the political information of the person currently logged in
        :return: the political information of the person currently logged in
        """

        person = self.request.person
        try:
            return person.politicalinformation
        except AttributeError:
            raise NotFound(
                detail='Associated political information not found.'
            )
