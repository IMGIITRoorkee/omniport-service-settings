from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from omniport.utils.switcher import load_serializer


class FinancialInformationView(generics.RetrieveUpdateAPIView,
                               generics.CreateAPIView):
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

    def partial_update(self, request, *args, **kwargs):

        person = self.request.person
        try:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        except:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(person_id=person.id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
