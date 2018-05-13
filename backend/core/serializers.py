from dynamic_rest.serializers import DynamicModelSerializer

from core.models import Item


class ItemSerializer(DynamicModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
