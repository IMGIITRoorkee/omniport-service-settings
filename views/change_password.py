from rest_framework import status, generics, permissions, response

from settings.serializers.change_password import (
    ChangePasswordSerializer,
)


class ChangePasswordView(generics.GenericAPIView):
    """
    This view takes the old password and the new password and if the old
    password is correct, changes the password to the new one

    Works only when authenticated
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data.get('new_password')
            user = request.user
            user.set_password(new_password)
            user.failed_reset_attempts = 0
            user.save()
            response_data = {
                'status': 'Successfully changed password.',
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_200_OK
            )
        else:
            response_data = {
                'errors': serializer.errors,
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
