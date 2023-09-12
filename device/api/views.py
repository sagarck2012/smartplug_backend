import csv
import datetime
import json
from itertools import chain

import pytz
from django.db.models import Max, Sum
# from django.db.models import Count, Max, Sum
# from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

# from django.db import connection
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.parsers import JSONParser

from device.api.serializers import DeviceSerializer, DeviceListSerializer, DeviceRegSerializerList
from device.models import Device, DeviceReg, TempDevice
import logging

logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deviceList(request):
    logging.debug(f'{datetime.datetime.now()}::Device List')
    if request.method == 'GET':
        devices = Device.objects.raw(
            'SELECT d.id, MAX(d.created_at) AS created_at, d.device_id, SUM(energy_consumption) as energy_consumption, c.value, dr.location, dr.status, dr.today_total, dr.yesterday_total, d.is_powered, d.total_consumption, d.is_connected_id FROM ((device_data AS d INNER JOIN device_connection AS c ON d.is_connected_id = c.id)INNER JOIN device_reg AS dr ON d.device_detail_id = dr.id) GROUP BY d.device_id ORDER BY device_id ASC, created_at ASC')
        # devicess = DeviceReg.objects.values('device_id', 'location', 'device__is_connected__device',).annotate(created_at=Max('device__timestamp'), energy_consumption=Sum('device__energy_consumption'))
        # sdevice = Device.objects.values('device_id', 'device_detail__location', 'energy_consumption').annotate(Count('device_id'), timestamp=Max('timestamp'), d=Count('device_detail'))
        # print(devicess)
        devicess = DeviceReg.objects.all().order_by('status')
        list_serializer = DeviceRegSerializerList(devicess, many=True)
        # print(len(sdevice))
        # sdevices = DeviceListSerializer(devicess, many=True)
        # print(sdevices.data)
        serializer = DeviceListSerializer(devices, many=True)
        print(serializer.data)
        return JsonResponse(list_serializer.data, safe=False)
    else:
        return HttpResponse(status=404)

    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = DeviceSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deviceDetail(request, pk):
    logging.debug(f'{datetime.datetime.now()}::Device Detail')
    if request.method == 'GET':
        date_t = datetime.datetime.today().date()
        try:
            device = TempDevice.objects.filter(device_id=pk).order_by('-created_at')
            # print(device) , created_at__gte=date_t
            serializer = DeviceSerializer(device, many=True)
            # print(serializer.data)
            return JsonResponse(serializer.data, status=200, safe=False)
        except Device.DoesNotExist:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_deviceList(request):
    logging.debug(f'{datetime.datetime.now()}::All Device List')
    if request.method == 'GET':
        try:
            # devices = Device.objects.all().order_by('created_at')
            date_t = datetime.datetime.today().date()
            # print(date_t)
            # p_devices = Device.objects.all().order_by('-created_at')
            # print(p_devices)
            print('--------------------')
            n_devices = TempDevice.objects.all().order_by('-created_at')
            print(n_devices)
            # sdevices = list(chain(n_devices, p_devices))
            # print(sdevices)
            # sdevices = Device.objects.filter().order_by('created_at')
            # paginator = PageNumberPagination()created_at__gte=date_t
            # paginator.page_size = 10
            # result_page = paginator.paginate_queryset(devices, request)
            # serializer = DeviceSerializer(devices, many=True)
            print('-----------======================================-')
            serializer2 = DeviceSerializer(n_devices, many=True)
            print('serialized data--------------', serializer2.data)
            return JsonResponse(serializer2.data, safe=False)
        except Device.DoesNotExist:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def device_list_filter(request):
    logging.debug(f'{datetime.datetime.now()}::Device List With Filter')
    data = json.loads(request.body)
    cur_date = datetime.datetime.today().date()
    from_str = data['fromDate'].split('T')
    to_str = data['toDate'].split('T')
    # from_date = datetime.datetime.strptime(from_str[0], "%Y-%m-%d").date()
    from_date = datetime.datetime.strptime(data['fromDate'].replace('T', " "), "%Y-%m-%d %H:%M")
    # to_date = datetime.datetime.strptime(to_str[0], "%Y-%m-%d").date()
    to_date = datetime.datetime.strptime(data['toDate'].replace('T', " "), "%Y-%m-%d %H:%M")
    print(cur_date, from_date, to_date)
    #     # print('from', data['fromDate'])
    #     # print(datetime.datetime.strptime(from_str[0], "%Y-%m-%d").date())
    if from_date.date() == cur_date and to_date.date() == cur_date:
        print('both current')
        devices = TempDevice.objects.filter(created_at__range=(from_date, to_date + datetime.timedelta(minutes=1))).order_by('-created_at')
    elif from_date.date() < cur_date and to_date.date() == cur_date:
        print('in prev day and today')
        p_devices = Device.objects.filter(created_at__gte=from_date).order_by('-created_at')
        n_devices = TempDevice.objects.filter(created_at__lte=to_date + datetime.timedelta(minutes=1)).order_by('-created_at')
        # print(n_devices)
        devices = list(chain(n_devices, p_devices))
    elif from_date.date() < cur_date and to_date.date() < cur_date:
        print('both other')
        devices = Device.objects.filter(created_at__range=(from_date, to_date + datetime.timedelta(minutes=1))).order_by('-created_at')
        # print(devices)
    elif from_date.date() < cur_date and to_date.date() >= cur_date:
        print('higher other')
        p_devices = Device.objects.filter(created_at__gte=from_date).order_by('-created_at')
        n_devices = TempDevice.objects.filter(created_at__lte=to_date).order_by('-created_at')
        # print(p_devices, n_devices)
        devices = list(chain(n_devices, p_devices))
    # devices = Device.objects.filter(created_at__range=(data['fromDate'], data['toDate'])).order_by('created_at')
    # print(devices)
    serializer = DeviceSerializer(devices, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def device_filter(request, pk):
    # print('req')
    logging.debug(f'{datetime.datetime.now()}::Device Filter')
    data = json.loads(request.body)
    cur_date = datetime.datetime.today().date()
    # cur_date = datetime.datetime.now()
    # print('under today')
    from_str = data['fromDate'].split('T')
    to_str = data['toDate'].split('T')
    # print(datetime.datetime.strptime(data['fromDate'].replace('T', " "), "%Y-%m-%d %H:%M"))
    # from_date = datetime.datetime.strptime(from_str[0], "%Y-%m-%d").date()
    from_date = datetime.datetime.strptime(data['fromDate'].replace('T', " "), "%Y-%m-%d %H:%M")
    # print('under from_date', from_date)
    # to_date = datetime.datetime.strptime(to_str[0], "%Y-%m-%d").date()
    to_date = datetime.datetime.strptime(data['toDate'].replace('T', " "), "%Y-%m-%d %H:%M")
    # print('under to_date', to_date)
    # print(cur_date, from_date, to_date)
    # print(cur_date)
    #     # print('from', data['fromDate'])
    #     # print(datetime.datetime.strptime(from_str[0], "%Y-%m-%d").date())
    # p_devices = Device.objects.filter(created_at__gte=from_date,  device_id=pk).order_by('-created_at')
    # n_devices = TempDevice.objects.filter(created_at__lte=to_date,  device_id=pk).order_by('-created_at')
    # devices = list(chain(n_devices, p_devices))
    if from_date.date() == cur_date and to_date.date() == cur_date:
        print('both current')
        devices = TempDevice.objects.filter(created_at__range=(from_date, to_date + datetime.timedelta(minutes=1)),
                                            device_id=pk).order_by('-created_at')
    elif from_date.date() < cur_date and to_date.date() == cur_date:
        print('in prev day and today')
        p_devices = Device.objects.filter(created_at__gte=from_date, device_id=pk).order_by('-created_at')
        n_devices = TempDevice.objects.filter(created_at__lte=to_date+ datetime.timedelta(minutes=1), device_id=pk).order_by('-created_at')
        # print(n_devices)
        devices = list(chain(n_devices, p_devices))
    elif from_date.date() < cur_date and to_date.date() < cur_date:
        print('both other')
        devices = Device.objects.filter(created_at__range=(from_date, to_date + datetime.timedelta(minutes=1)),
                                        device_id=pk).order_by('-created_at')
        # print(devices)
    elif from_date.date() < cur_date and to_date.date() >= cur_date:
        print('higher other')
        p_devices = Device.objects.filter(created_at__gte=from_date, device_id=pk).order_by('-created_at')
        n_devices = TempDevice.objects.filter(created_at__lte=to_date, device_id=pk).order_by('-created_at')
        # print(p_devices, n_devices)
        devices = list(chain(n_devices, p_devices))
    # devices = Device.objects.filter(created_at__range=(data['fromDate'], data['toDate']), device_id=pk).order_by('created_at')
    # print(devices)
    serializer = DeviceSerializer(devices, many=True)
    # print(serializer.data)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def device_reg(request):
    logging.debug(f'{datetime.datetime.now()}::Device Reg')
    data = json.loads(request.body)
    location = data['location']
    device_id = data['device_id']
    print(data)
    device_no_str = device_id.split('_')[1]
    print(device_no_str)
    sensor_id = 'dev_' + device_no_str[2:]
    print(sensor_id)

    device = DeviceReg.objects.update_or_create(device_id=device_id, sensor_id=sensor_id,
                                                defaults={"location": location, })
    manu_device = DeviceReg.objects.get(device_id=device_id)
    print(manu_device)
    return JsonResponse({'status': device[1], 'device_id': manu_device.device_id}, safe=False)

TOKEN = '0d514d6722ef49698ac450eb4c9eadc7'

@api_view(['POST'])
@authentication_classes([])
def csv_data_all(request):
    logging.debug(f'{datetime.datetime.now()}::CSV Data')
    print(datetime.datetime.now())
    print(request.body)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=data.csv'
    writer = csv.writer(response)
    device_data = None
    if request.body:
        body_data = json.loads(request.body)
        logging.debug(f'{datetime.datetime.now()}::CSV Data:: {body_data}:: {str(request.headers)}')
        try:
            token = body_data['token']
            date = body_data['date']
            to_date = body_data['to_date']
            date_arr = date.split('-')
            year = date_arr[0]
            month = date_arr[1]
            day = date_arr[2]
            print(body_data)
            if 'device_id' in body_data:
                device_id = body_data['device_id']
                response['Content-Disposition'] = f'attachment; filename={device_id}.csv'
                if 'to_date' in body_data:
                    # print('in if', type(date), to_date)
                    to_date_d = datetime.datetime.strptime(to_date, '%Y-%m-%d') + datetime.timedelta(hours=24)
                    date_d = datetime.datetime.strptime(date, '%Y-%m-%d')
                    # print(to_date_d, date_d)
                    device_data = Device.objects.values().filter(created_at__range=(date_d, to_date_d),
                                            device_id=device_id).order_by('created_at')
                else:
                    device_data = Device.objects.values().filter(created_at__year=year, created_at__month=month,
                                                             created_at__day=day, device_id=device_id).order_by('created_at')
            else:
                cur = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M")
                cur_str = 'all_device_' + str(cur).replace(', ', '_').replace('/', '_').replace(':', '_')
                print(cur_str)
                response['Content-Disposition'] = f'attachment; filename={cur_str}.csv'
                if 'to_date' in body_data:
                    to_date_d = datetime.datetime.strptime(to_date, '%Y-%m-%d') + datetime.timedelta(hours=24)
                    date_d = datetime.datetime.strptime(date, '%Y-%m-%d')
                    device_data = Device.objects.values().filter(created_at__range=(date_d, to_date_d)).order_by('created_at')
                else:
                    device_data = Device.objects.values().filter(created_at__year=year, created_at__month=month,
                                                             created_at__day=day).order_by('created_at')

            writer.writerow(['Created At', 'Device Id', 'Energy Usage (w/h)', 'Internet', 'Power'])

            for device in device_data:
                connected = 'Connected' if device['is_connected_id'] == 1 else 'Disconnected'
                powered = 'Connected' if device['is_powered'] is True else 'Disconnected'
                # created_time = datetime.datetime.strptime(str(device['created_at']), '%d/%m/%Y %H:%M')
                created_time = device['created_at'].strftime("%m/%d/%Y %H:%M")
                # print(created_time)
                writer.writerow([created_time, device['device_id'], device['energy_consumption'], connected, powered])
        except Exception as e:
            return HttpResponse(json.dumps({'message': 'Invalid Token'}), content_type='application/json')

    else:
        print('empty')

    return response
