from datetime import datetime

from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from omniport.utils.switcher import load_serializer


class BiologicalInformationView(generics.RetrieveUpdateAPIView,
                                generics.CreateAPIView):
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
                detail='Associated biological information not found.',
            )

    def partial_update(self, request, *args, **kwargs):
        """
        Update the biological information of the person currently logged in
        :return: Updated instance
        """
        
        person = self.request.person
        try:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        except:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                dob = request.data['date_of_birth']
                dob = datetime.strptime(dob, "%d-%m-%Y").strftime("%Y-%m-%d")
            except KeyError:
                return Response({
                    'Date of Birth': ['This field is required']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(person_id=person.id, date_of_birth=dob)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )

    def options(self, request, *args, **kwargs):
        """
        Handler method for HTTP OPTIONS request.
        """

        if self.metadata_class is None:
            return self.http_method_not_allowed(request, *args, **kwargs)
        data = self.metadata_class().determine_metadata(request, self)
        return Response(data, status=status.HTTP_200_OK)
