from rest_framework import serializers
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from .models import AccountDetails

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("name", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def save(self):
        user = get_user_model()(
            email=self.validated_data["email"],
            name=self.validated_data["name"],
        )

        password = self.validated_data["password"]


        user.set_password(password)
        user.save()

        AccountDetails.objects.create(user=user)
        return user

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region="NG")

class AccountSerializer(serializers.ModelSerializer):
    # user_profile = UserProfileSerializer(required=False)
    phone_number = PhoneNumberField(region="NG", required=False)

    class Meta:
        model = get_user_model()
        fields = ("id","name", "email", "phone_number")
        read_only_fields = ['email']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDetails
        fields = "__all__"