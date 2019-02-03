from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from omniport.utils.switcher import load_serializer


class BiologicalInformationView(generics.RetrieveUpdateAPIView):
    """
    View for RU operations on biological information
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = load_serializer('kernel', 'BiologicalInformation')

    def get_object(self):
        """
        Return the biological information of the person currently logged in
        :return: the biological information of the person currently logged in
        """

        person = self.request.person
        try:
            return person.biologicalinformation
        except AttributeError:
            raise NotFound(
                detail='Associated biological information not found.'
            )
