from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    """
    Stores the old and the new password for a user intending to change it
    """

    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_old_password(self, old_password):
        """
        Validates the old password by checking if it authenticates the user
        :param old_password: the old password for a user
        :return: the old password if it authenticates the user
        :raise serializers.ValidationError: if the old password is incorrect
        """

        user = self.context.get('request').user

        if not user.check_password(old_password):
            raise serializers.ValidationError('Incorrect old password')

        return old_password
