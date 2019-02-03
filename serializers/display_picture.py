import swapper
from rest_framework import serializers

Person = swapper.load_model('kernel', 'Person')


class DisplayPictureSerializer(serializers.ModelSerializer):
    """
    Serializer for the display picture field of Person objects
    """

    class Meta:
        """
        Meta class for DisplayPictureSerializer
        """

        model = Person
        fields = [
            'display_picture',
        ]
