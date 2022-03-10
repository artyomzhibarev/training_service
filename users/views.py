from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateCustomerSerializer


class CreateCustomerAPIView(GenericAPIView):
    serializer_class = CreateCustomerSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            email = serializer.data.get('email')
            token = Token.objects.get(user=user).key
            data = {
                'email': email,
                'token': token
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutCustomerAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        Token.objects.get(user=request.user).delete()
        # request.user.token.delete()
        data = {
            'message': f'The user {request.user} successfully logout'
        }
        return Response(data=data, status=status.HTTP_200_OK)
