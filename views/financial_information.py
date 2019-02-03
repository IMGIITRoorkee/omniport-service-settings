from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from omniport.utils.switcher import load_serializer


class FinancialInformationView(generics.RetrieveUpdateAPIView):
    """
    View for RU operations on financial information
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = load_serializer('kernel', 'FinancialInformation')

    def get_object(self):
        """
        Return the financial information of the person currently logged in
        :return: the financial information of the person currently logged in
        """

        person = self.request.person
        try:
            return person.financialinformation
        except AttributeError:
            raise NotFound(
                detail='Associated financial information not found.'
            )
