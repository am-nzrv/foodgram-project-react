from rest_framework import viewsets, mixins

from api.permissions import IsAdminOrReadOnly


class ListRetrieveViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin):
    permission_classes = (IsAdminOrReadOnly, )