from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from settings.serializers.session_map import SessionMapSerializer


class SessionMapViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset for listing and destroying SessionMap objects
    """

    permission_classes = [IsAuthenticated, ]
    serializer_class = SessionMapSerializer
    pagination_class = None

    def perform_destroy(self, instance):
        """
        Clear the session key from a SessionMap instance and then defer to the
        parent implementation to actually delete the instance
        :param instance: the SessionMap instance to destroy
        """

        instance.clear_session()
        return super().perform_destroy(instance)

    def get_queryset(self):
        """
        Get the list of all SessionMap objects attached with a particular user
        :return: the list of all user SessionMap objects
        """

        return self.request.user.sessionmap_set.all()
