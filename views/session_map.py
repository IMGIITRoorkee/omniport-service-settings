from importlib import import_module

from django.conf import settings
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

        session_key = instance.session_key
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore(session_key=session_key)
        session.delete()

        return super().perform_destroy(instance)

    def get_queryset(self):
        """
        Get the list of all SessionMap objects attached with a particular user
        :return: the list of all user SessionMap objects
        """

        user = self.request.user
        return user.sessionmap_set.all().order_by('-datetime_modified')
