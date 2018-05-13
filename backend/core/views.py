from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework.permissions import AllowAny

from core.models import Item
from core.serializers import ItemSerializer


class ItemViewSet(DynamicModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = (AllowAny,)
