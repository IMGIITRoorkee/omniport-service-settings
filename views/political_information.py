from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from django_countries import countries

from omniport.utils.switcher import load_serializer
from shell.constants import reservation_categories


class PoliticalInformationView(generics.RetrieveUpdateAPIView,
                               generics.CreateAPIView):
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

    def partial_update(self, request, *args, **kwargs):
        """
        Update the political information of the person currently logged in
        :return: Updated instance
        """

        person = self.request.person
        try:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        except:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = request.data

            try:
                nationality=data['nationality']
            except KeyError:
                return Response({
                    'Nationality': ['This field is required']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                aadhaar_card_number=data['aadhaar_card_number']
            except KeyError:
                return Response({
                    'Aadhar card no.': ['This field is required']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                reservation_category=data['reservation_category']
            except KeyError:
                return Response({
                    'Reservation Category': ['This field is required']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(
                person_id=person.id,
                aadhaar_card_number=aadhaar_card_number,
                reservation_category=reservation_category,
                nationality=nationality,
            )
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )

    def options(self, request, *args, **kwargs):
        """
        Handler method for HTTP OPTIONS request.
        """

        if self.metadata_class is None:
            return self.http_method_not_allowed(request, *args, **kwargs)
        data = self.metadata_class().determine_metadata(request, self)
        data['actions']['POST']['aadhaar_card_number']['read_only'] = False
        return Response(data, status=status.HTTP_200_OK)
