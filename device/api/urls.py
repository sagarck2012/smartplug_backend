from django.urls import path

from device.api import views

urlpatterns = [
    path('devices/', views.deviceList),
    path('all-devices/', views.all_deviceList),
    path('all-devices-with-dateRange/', views.device_list_filter),
    path('devices/<str:pk>', views.deviceDetail),
    path('devices-with-dateRange/<str:pk>', views.device_filter),
    path('device-reg/', views.device_reg),
    path('download/', views.csv_data_all),
]
