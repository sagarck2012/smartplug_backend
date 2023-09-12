import base64

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # implement your logic here
        # print(type(attrs), attrs['username'], attrs['password'],)
        password = attrs['password'].encode("ascii")
        password_sb = base64.b64decode(password)
        password_s = password_sb.decode("ascii")
        # print(password_s)
        attrs['password'] = password_s
        data = super().validate(attrs)
        return data

    # def __setattr__(self, key, value):
    #     # print(self.data, self.initial_data)
    #     print(f'key=={key}::value=={value}::')
    #     # print(value[1])
    # def __getattr__(self, item):
    #     print(item.initial_data)
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['name'] = user.first_name + ' ' + user.last_name
        token['is_staff'] = user.is_staff
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'api/token/',
        'api/token/refresh',
    ]
    return Response(routes)
