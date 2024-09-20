from rest_framework.decorators import api_view, permission_classes
from rest_framework import response, exceptions as rest_exceptions, permissions as rest_permissions, status
from . import serializers, models
from rest_framework_simplejwt import tokens,  serializers as jwt_serializers, exceptions as jwt_exceptions, views as jwt_views
from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import authenticate, get_user_model

def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }

@api_view(['POST'])
def login_view(request):
    serializer = serializers.LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = authenticate(email=email, password=password)

    if user is not None:
        tokens = get_user_tokens(user)
        res = response.Response()
        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens["access_token"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=tokens["refresh_token"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        response_obj = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
        }
        res.data = response_obj

        res["X-CSRFToken"] = csrf.get_token(request)
        return res
    raise rest_exceptions.AuthenticationFailed(
        "Incorrect email or password")

@api_view(["POST"])
def register_view(request):
    serializer = serializers.RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    if user is not None:
        return response.Response("Registered!")
    return rest_exceptions.AuthenticationFailed("Invalid credentials!")

@api_view(['POST'])
@permission_classes([rest_permissions.IsAuthenticated])
def logoutView(request):
    try:
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        token = tokens.RefreshToken(refreshToken)
        token.blacklist()

        res = response.Response()
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        res.delete_cookie("X-CSRFToken")
        res.delete_cookie("csrftoken")
        res["X-CSRFToken"]=None
        
        return res
    except:
        raise rest_exceptions.ParseError("Invalid token")


class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise jwt_exceptions.InvalidToken(
                'No valid token found in cookie \'refresh\'')


class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=response.data['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)


@api_view(["GET"])
@permission_classes([rest_permissions.IsAuthenticated])
def user(request):
    try:
        user = models.Account.objects.get(id=request.user.id)
    except models.Account.DoesNotExist:
        return response.Response(status_code=404)

    serializer = serializers.AccountSerializer(user)
    return response.Response(serializer.data)

@api_view(["POST"])
def reset_password_view(request, token):
    serializer = serializers.ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    password = data["new_password"]
    confirm_password = data["confirm_password"]

    if password != confirm_password:
            return response.Response({"error": "Passwords do not match"}, status=400)
        
    reset_obj = models.PasswordReset.objects.filter(token=token).first()
        
    if not reset_obj:
        return response.Response({'error':'Invalid token'}, status=400)
        
    user = models.Account.objects.filter(email=reset_obj.email).first()
        
    if user:
        user.set_password(request.data['new_password'])
        user.save()
            
        reset_obj.delete()
            
        return response.Response({'success':'Password updated'})
    else: 
        return response.Response({'error':'No user found'}, status=404)

@api_view(["GET", "PUT"])
@permission_classes([rest_permissions.IsAuthenticated])
def user_view(request):
    if request.method == 'GET':
        try:
            user = models.Account.objects.get(id=request.user.id)

        except models.Account.DoesNotExist:
            return response.Response(status=404)
        
        serializer = serializers.AccountSerializer(user)
        response_obj = {**serializer.data, "user_details": serializers.UserDetailsSerializer(user.user_details).data}

        return response.Response(response_obj)

    if request.method == 'PUT':
        user = request.user
        serializer = serializers.AccountSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.data)


@api_view(['DELETE'])    
def delete_user_view(request, user_id):
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    
    user.delete()
    res = response.Response(status=status.HTTP_204_NO_CONTENT)
    res.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
    res.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
    res.delete_cookie("X-CSRFToken")
    res.delete_cookie("csrftoken")
    res["X-CSRFToken"] = None
    return res
