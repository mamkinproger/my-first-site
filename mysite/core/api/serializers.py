from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from mysite.core.models import Device, DeviceStandart, DeviceStandartToDevice


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=6, max_length=128, write_only=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    def create(self, validated_date):
        user = User.objects.create_user(username=validated_date['username'],
                                        email=validated_date['email'],)
        user.set_password(validated_date['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class DevToDevSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceStandartToDevice
        fields = ('deviceid', 'devicestandartid')


class DeviceStandartSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceStandart
        fields = 'type'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'standarts', 'state', 'name')

# class DeviceListStopSerializer(serializers.ListSerializer):
#     def update(self, instance, validated_data):


class ListStopSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        device_mapping = {Device.objects.id: device for device in instance}
        data_mapping = {item['id']: item for item in validated_data}
        ret = []
        for device_id, data in data_mapping.items():
            device = device_mapping.get(Device.objects.id, None)
            if device is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(device, data))
        return ret


class DeviceStopSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    standarts = serializers.ListField(child=serializers.IntegerField(min_value=1, max_value=5))
    state = serializers.IntegerField(min_value=0, max_value=2)
    name = serializers.CharField()

    class Meta:
        model = Device
        fields = ('id', 'standarts', 'state', 'name')
        list_serializer_class = ListStopSerializer

    def validate_state(self, value):
        if value != 2:
            raise serializers.ValidationError("Одно или несколько устройств уже выключены или недоступны")
        return value

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.standarts = validated_data.get('standart', instance.standarts)
        instance.state = 1
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


    # def validate(self, validated_data):
    #     if self.context['request'].method == 'post':
    #         validated_data['state'] = self.context['request'].data.get('state')
    #         if validated_data['state'] != 2:
    #             raise serializers.ValidationError("Одно или несколько устройств уже выключены или недоступны")
    #         return validated_data
    # def save(self, **kwargs):
    #     validated_data = self.validated_data(**kwargs)
    #     if self.instance is not None:
    #         self.instance = self.update(self.instance, validated_data)
    #     return self.instance

    # def partial_update(self, instance, validated_data):
    #     instance.state = validated_data['state']
    #     instance.save()
    #     return instance

    # def update(self, instance, validated_data):
    #
    #     info = Device(instance)
    #     for state in validated_data.items():
    #         if state in info.state:
    #             field = getattr(instance, state)
    #             field.set(state=1)
    #         else:
    #             setattr(instance, state, 1)
    #     instance.save()
    #     return instance








