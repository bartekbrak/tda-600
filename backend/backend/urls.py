from django.http import HttpResponse
from django.urls import path
from dynamic_rest.routers import DynamicRouter

from core.views import ItemViewSet

router = DynamicRouter()
router.register(r'items', ItemViewSet, base_name='items')
urlpatterns = router.urls

urlpatterns += [
    path('favicon.ico', lambda request: HttpResponse('empty')),
]
