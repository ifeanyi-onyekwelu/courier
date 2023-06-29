from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('packaging/', views.allPackaging, name="all_packaging"),
    path('delivered/', views.allDelivered, name="all_delivered"),
    path('intransit/', views.allInTransit, name="all_in_transit"),
    path('shipping/', views.allShipping, name="all_shipping"),
    path('dispatch/', views.alldispatchs, name="all_dispatch"),

    # ===================
    # One item urls
    # ===================
    path('dispatch/<uuid:pk>/', views.dispatch, name="dispatch"),
    path('update/<uuid:pk>/', views.updateParcel, name="update_parcel"),

    # ===================
    # Coupon urls
    # ===================
    path('coupon/', views.allCoupons, name="all_coupons"),
    path('create-coupon/', views.create_coupon, name="create_coupon"),
    path('delete-coupon/<int:pk>/', views.deleteCoupon, name="delete_coupon"),

    # ===================
    # Authentication urls
    # ===================
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('notLoggedIn/', views.notLoggedIn, name="not_logged_in"),

    # ===================
    # Profile urls
    # ===================
    path('profile/', views.profile, name="profile"),
    path('edit/', views.editProfile, name="edit_profile"),
    path('changepassword/', views.changePassword, name="change_password"),


    path('check_updates/', views.check_updates, name='check_updates'),
]