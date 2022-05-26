from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from omniport.utils.switcher import load_serializer

import swapper


Residence = swapper.load_model('kernel', 'Residence')

class ResidentialInformationView(generics.RetrieveUpdateAPIView,
                                 generics.CreateAPIView):
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

    def partial_update(self, request, *args, **kwargs):
        """
        Update the residential information of the person currently logged in
        :return: Updated instance
        """

        person = self.request.person
        try:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        except:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            residence = request.data['residence']
            residence = Residence.objects.get(pk=residence)
            serializer.save(person_id=person.id, residence=residence)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
