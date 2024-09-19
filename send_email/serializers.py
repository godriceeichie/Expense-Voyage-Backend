from rest_framework import serializers

class ResetPasswordLinkSerializer(serializers.Serializer):
    email = serializers.EmailField()