from django.contrib.auth.models import User
from users.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request):
    return Response({
        'users': reverse('user-list', request=request),
    })