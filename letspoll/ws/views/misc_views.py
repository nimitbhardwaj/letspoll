from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.conf import settings

class MiscViews(ViewSet):
    def get_version(self, req):
        return Response({'version': settings.VERSION})