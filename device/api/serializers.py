from rest_framework import serializers

from device.models import Device, DeviceReg




class DeviceRegSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceReg
        fields = ['location']


class DeviceRegSerializerList(serializers.ModelSerializer):
    class Meta:
        model = DeviceReg
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):

    is_connected = serializers.SlugRelatedField(slug_field='value', read_only=True, many=False)
    device_detail = DeviceRegSerializer()



    class Meta:
        model = Device
        fields = ['device_id', 'energy_consumption', 'created_at', 'is_connected', 'device_detail', 'is_powered', 'total_consumption']


class DeviceListSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField('get_status')
    device_detail = serializers.SerializerMethodField('get_location')
    is_connected = serializers.SerializerMethodField('get_connected')
    yesterday_total = serializers.SerializerMethodField('get_yesterday_total')
    today_total = serializers.SerializerMethodField('get_today_total')
    total_consumption = serializers.SerializerMethodField('get_total_consumption')

    # print(is_connected, device_detail)

    # def get_is_connected(self, obj):
    #     # print(obj.vallue)
    #     return obj.value
    #
    #
    def get_connected(self, obj):
        # print(obj.location)
        return obj.value

    def get_location(self, obj):
        # print(obj.location)
        return obj.location

    def get_status(self, obj):
        # print(obj.location)
        return obj.status

    def get_yesterday_total(self, obj):
        return obj.yesterday_total

    def get_today_total(self, obj):
        return obj.today_total

    def get_total_consumption(self, obj):
        return obj.total_consumption

    class Meta:
        model = Device
        fields = ['device_id', 'created_at', 'device_detail', 'energy_consumption', 'is_connected', 'yesterday_total', 'today_total', 'total_consumption', 'is_powered', 'status']
