# test for API browser
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import api_view, list_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from mysite.core.api.serializers import UserSerializer, DeviceSerializer, DeviceStopSerializer
from mysite.core.models import Device
from django.shortcuts import get_object_or_404
from django.db.models import Q
import operator
from rest_framework.mixins import ListModelMixin


class HalloList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()



class GetDeviceStates(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()


# class MultipleFieldLookupMixin(object):
#     def get_object(self):
#         queryset = self.get_queryset()  # Get the base queryset
#         queryset = self.filter_queryset(queryset)  # Apply any filter backends
#         filter = {}
#         for field in self.lookup_fields:
#             if self.kwargs[field]:  # Ignore empty fields.
#                 filter[field] = self.kwargs[field]
#         obj = get_object_or_404(queryset, **filter)  # Lookup the object
#         self.check_object_permissions(self.request, obj)
#         return obj


class StopDeviceView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = DeviceStopSerializer
    queryset = Device.objects.all

    def get_queryset(self):
        queryset_list = Device.objects.all()
        return queryset_list

    def get(self, request):
        queryset = Device.objects.all(request)
        serializer = DeviceStopSerializer(queryset, many=True)
        return Response(serializer.data)

    def put(self, request):
        serializer = DeviceStopSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "BLLAAAAAAT< NAKANEZTA"}, status.HTTP_200_OK)
        return Response({"error": "SORYAN BRO"}, status.HTTP_400_BAD_REQUEST)

# class StopDevicesViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
#                          mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    # @list_route(methods=['post'])
    # def update(self, request, *args, **kwargs):
    # queryset = Device.objects.all()
    # serializer_class = DeviceStopSerializer
    # serializer_class = DeviceStopSerializer
    # lookup_field = ('pk', 'state')
    # def post(self, request, pk, format=None):
    #     Device = self.get_object(pk)
    #     serializer = DeviceStopSerializer(Device, data=request.data, context={"request": request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "BLLAAAAAAT< NAKANEZTA"}, status.HTTP_200_OK)
    #     return Response({"error": "SORYAN BRO"}, status.HTTP_400_BAD_REQUEST)

    # @list_route(methods=['post'])
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
        # self.queryset = Device.objects.all()
        # self.serializer_class = DeviceStopSerializer
        # data = {
        #     'id': request.data['id'],
        #     'standarts': request.data['standarts'],
        #     'state': request.data['state'],
        #     'name': request.data['name']
        # }
        # instances = {
        #     'id': request.data['id'],
        #     'standarts': request.data['standarts'],
        #     'state': 1,
        #     'name': request.data['name']
        # }
        # serializer = DeviceStopSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({"message": "BLLAAAAAAT< NAKANEZTA"}, status.HTTP_200_OK)
        # return Response({"error": "SORYAN BRO"}, status.HTTP_400_BAD_REQUEST)

    # def stop(self, request):
    #     serializer = DeviceStopSerializer(data=request.data, many=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "BLLAAAAAAT< NAKANEZTA"}, status.HTTP_200_OK)
    #     return Response({"error": "SORYAN BRO"}, status.HTTP_400_BAD_REQUEST)


class StartDevices(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceSerializer

    def post(self, request):
        request = DeviceSerializer(data=request.data, many=True)
        if request.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(request.errors, status.HTTP_400_BAD_REQUEST)


class UserCreate(APIView):
    def post(self, request, format = 'json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Login failed"}, status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})




