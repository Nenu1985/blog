from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import GroupSerializer, UserSerializer
from .tasks import sleep as celery_sleep
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
def sleep(request, sec: int):
    """
    List all code snippets, or create a new snippet.
    """
    # print('Sleep task is called')
    logger.info('Sleep task is called!')
    celery_sleep.delay(sec)
    logger.info(f'Sleep task has slept for {sec} seconds.')
    return Response({'response': 'went to sleep'})