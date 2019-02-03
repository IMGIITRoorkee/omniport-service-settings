from rest_framework import status, generics, permissions, response

from settings.serializers.change_secrets import (
    ChangeSecretsSerializer,
)


class ChangeSecretsView(generics.GenericAPIView):
    """
    This view takes the old password and the secret question and answer and
    if the old password is correct, changes the question and answers to the new
    ones

    Works only when authenticated
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ChangeSecretsSerializer

    def get(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        user = request.user
        secret_question = user.secret_question
        response_data = {
            'secret_question': secret_question,
        }
        return response.Response(
            data=response_data,
            status=status.HTTP_200_OK
        )

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
            secret_question = serializer.validated_data.get('secret_question')
            secret_answer = serializer.validated_data.get('secret_answer')

            user = request.user
            if secret_question is not None and secret_question != '':
                user.secret_question = secret_question
            if secret_answer is not None and secret_answer != '':
                user.set_secret_answer(secret_answer)
            user.failed_reset_attempts = 0
            user.save()

            response_data = {
                'status': 'Successfully changed secrets.',
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
