from django.conf.urls import url, include
from .views import login, UserCreate, HalloList, GetDeviceStates, StopDeviceView, StartDevices
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'stop', StopDeviceViewSet, base_name='stop')

urlpatterns = [
    url(r'^hallo', HalloList.as_view(), name="hallo"),
    url(r'^login', login),
    url(r'^signup', UserCreate.as_view(), name="signup'"),
    url(r'^states', GetDeviceStates.as_view(), name="states"),
    # url(r'^stop', StopDeviceViewSet.as_view({'post': 'partial_update', 'put': 'update'}), name="stop"),
    url(r'^stop', StopDeviceView.as_view(), name="stop"),
    url(r'^start', StartDevices.as_view(), name="start"),
    # url(r'^', include(router.urls)),
    ]

