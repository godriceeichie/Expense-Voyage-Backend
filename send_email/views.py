from rest_framework.decorators import api_view
from . import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.models import PasswordReset
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from rest_framework.response import Response

# Create your views here.

Account = get_user_model()

@api_view(["POST"])
def password_reset_link_email(request):
    serializer = serializers.ResetPasswordLinkSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email_address = serializer.validated_data["email"]

    user = Account.objects.filter(email__iexact=email_address).first()

    if user:
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        reset = PasswordReset(email=email_address, token=token)
        reset.save()

        context = {'name': user.name, 'reset_link': f"http://localhost:5173/auth/reset-password/{token}"}
        html_message=render_to_string("send_email/password_reset.html", context=context)

        email = EmailMessage(
            subject="Password Reset",
            body=html_message,
            from_email="techsyndicate001@gmail.com",
            to=[request.data.get("email")],
            reply_to=[email_address],
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        messages.success(request, "Email has been sent successfully")
        return Response("Email sent successfully")
    
    else:
        return Response({"error": "User with credentials not found"}, status=404)

