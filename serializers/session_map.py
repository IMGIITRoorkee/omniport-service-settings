from rest_framework import serializers

from session_auth.models import SessionMap


class SessionMapSerializer(serializers.ModelSerializer):
    """
    Serializer for SessionMap objects
    """

    current = serializers.SerializerMethodField()

    def get_current(self, instance):
        """
        Get whether the current instance being serialized is the session on
        which the user is logged in
        :param instance: the instance being serialized
        :return: True if the current session key matches this instance's
        """

        current_key = self.context.get('request').session.session_key
        this_key = instance.session_key
        return this_key == current_key

    class Meta:
        """
        Meta class for SessionMapSerializer
        """

        model = SessionMap
        exclude = [
            'session_key',
            'user_agent',
            'browser_version',
        ]
