from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from settings.serializers.display_picture import DisplayPictureSerializer


class DisplayPictureView(generics.RetrieveUpdateAPIView):
    """
    View for RU operations on display picture
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = DisplayPictureSerializer

    def get_object(self):
        """
        Return the person currently logged in
        :return: the person currently logged in
        """

        person = self.request.person
        if person is not None:
            return person
        else:
            raise NotFound(
                detail='Associated person not found.'
            )
