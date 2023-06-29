from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('', views.home, name="home_page"),
    path('dispatch-parcel/', views.dispatchPackage, name="dispatch_parcel"),
    path('track-package/', views.trackPackage, name="track_package"),
    path('get-package-info/', views.get_package_info, name='get_package_info'),
    path('view-package-status/', views.view_package_status, name='view_package_status'),
    # send email url
    path('send-message/', views.sendMessage, name="send_message"),
]