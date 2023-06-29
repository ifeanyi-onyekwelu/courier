from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.db.models import Count
from .decorators import admin_login_required
from app.models import Package
from django.db.models import Q
from . import utils
from .models import Coupon
import os
import datetime
from django.contrib.auth.hashers import make_password
from .management.commands.scheduler import has_updates


# Dashboard view
@admin_login_required
def dashboard(request):
    dispatchedPackages = Package.objects.order_by('-created_at')[:6]
    current_year = datetime.datetime.now().year

    # Query to get the counts of packages created and delivered per year
    package_count = (
        Package.objects.filter(created_at__year=current_year)
        .values("status")
        .annotate(count=Count("status"))
    )

    # Initialize variables for storing the count
    created_count = 0
    delivered_count = 0

    # Iterate over the package count and assign values to the variables
    for item in package_count:
        if item["status"] == "Delivered":
            delivered_count = item["count"]
        created_count += item["count"]

    context = {
        "created_count": created_count,
        "delivered_count": delivered_count,
        "dispatchedPackages": dispatchedPackages,
    }
    return render(request, "admin/index.html", context)


# Packaging view
@admin_login_required
def allPackaging(request):
    dispatchedPackages = Package.objects.all()

    context = {"dispatchedPackages": dispatchedPackages}
    return render(request, "admin/packaging.html", context)


# Delivered view
@admin_login_required
def allDelivered(request):
    dispatchedPackages = Package.objects.all()

    context = {"dispatchedPackages": dispatchedPackages}
    return render(request, "admin/delivered.html", context)


# In Transit view
@admin_login_required
def allInTransit(request):
    dispatchedPackages = Package.objects.all()

    context = {"dispatchedPackages": dispatchedPackages}

    return render(request, "admin/inTransit.html", context)


# Reviews view
@admin_login_required
def alldispatchs(request):
    dispatchedPackages = Package.objects.all()

    # Get filter values from request parameters
    month = request.GET.get("month")
    year = request.GET.get("year")
    query = request.GET.get("query")

    # Apply filters if provided
    if month:
        dispatchedPackages = dispatchedPackages.filter(created_at__month=month)
        print(
            "Filtered by Month:", dispatchedPackages.count()
        )  # Print the number of packages after month filtering
    if year:
        dispatchedPackages = dispatchedPackages.filter(created_at__year=year)
        print(
            "Filtered by Year:", dispatchedPackages.count()
        )  # Print the number of packages after month filtering
    if query:
        dispatchedPackages = dispatchedPackages.filter(
            Q(senderName__icontains=query) | Q(recipeintName__icontains=query)
        )
        print(
            "Filtered by Query:", dispatchedPackages.count()
        )  # Print the number of packages after query filtering

    if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        # Render the table content as a partial HTML response
        table_content = render_to_string(
            "_table_content.html", {"dispatchedPackages": dispatchedPackages}
        )
        return HttpResponse(table_content)

    context = {"dispatchedPackages": dispatchedPackages}
    return render(request, "admin/dispatch.html", context)


@admin_login_required
def dispatch(request, pk):
    dispatch = Package.objects.get(id=pk)
    dispatch_status = Package.STATUS

    context = {"dispatch": dispatch, "dispatchStatus": dispatch_status, "parcel": pk}
    return render(request, "admin/dispatched.html", context)


@admin_login_required
def updateParcel(request, pk):
    if request.method == "POST":
        status = request.POST.get("status")
        print(status)
        parcel = Package.objects.get(id=pk)
        print(parcel)

        parcel.status = status
        parcel.save()

        if parcel.status == "Packaging":
            email_subject = "Parcel is being packaged"
            email_body = utils.get_dispatch_packaging_content(parcel.senderName)
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [parcel.senderEmail],
                fail_silently=False,
            )
        elif parcel.status == "In Transit":
            email_subject = "Parcel is in transit"
            email_body = utils.get_dispatch_in_transit(parcel.senderName)
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [parcel.senderEmail],
                fail_silently=False,
            )
        elif parcel.status == "Shipping":
            email_subject = "Parcel is being shipped"
            email_body = utils.get_dispatch_shipped(parcel.senderName)
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [parcel.senderEmail],
                fail_silently=False,
            )
        elif parcel.status == "Delivered":
            email_subject = "Parcel has been delivered"
            email_body = utils.get_dispatch_delivered_content(parcel.senderName)
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [parcel.senderEmail],
                fail_silently=False,
            )

        return redirect(reverse("admin:dispatch", kwargs={"pk": str(pk)}))
    return render(request, "admin/dispatched.html")


# Shipping view
@admin_login_required
def allShipping(request):
    dispatchedPackages = Package.objects.all()

    context = {"dispatchedPackages": dispatchedPackages}

    return render(request, "admin/shipping.html", context)



@admin_login_required
def allCoupons(request):
    coupons = Coupon.objects.all()
    return render(request, "admin/coupon.html", {"coupons": coupons})

@admin_login_required
def deleteCoupon(request, pk):
    coupon = Coupon.objects.get(id=pk)

    if coupon is not None:
        coupon.delete()
        return redirect(reverse('admin:all_coupons'))


@admin_login_required
def create_coupon(request):
    newCoupon = Coupon.objects.create()
    newCoupon.save()
    return redirect(reverse("admin:all_coupons"))


# Profile view
@admin_login_required
def profile(request):
    return render(request, "admin/profile.html")


@admin_login_required
def editProfile(request):
    try:
        if request.method == "POST":
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            username = request.POST.get("username")
            email = request.POST.get("email")
            user = User.objects.get(id=request.user.id)

            if user is not None:
                user.first_name = firstName
                user.last_name = lastName
                user.username = username
                user.email = email
                user.save()
                return redirect(reverse("admin:edit_profile"))
        return render(request, "admin/profile.html")

    except Exception as e:
        messages.error(request, e)
        return redirect(reverse("admin:profile"))
    return render(request, "admin/profile.html")


@admin_login_required
def changePassword(request):
    try:
        if request.method == "POST":
            currentpassword = request.POST.get("currentpassword")
            newPassword = request.POST.get("newpassword")
            confirmPassword = request.POST.get("renewpassword")

            user = User.objects.get(id=request.user.id)

            if user is not None:
                if newPassword == confirmPassword:
                    if user.check_password(currentpassword):
                        user.password = make_password(newPassword)
                        user.save()
                        return redirect(reverse("admin:change_password"))
                    else:
                        messages.error(request, "current password is incorrect")
                        return redirect(reverse("admin:change_password"))
                else:
                    messages.error(request, "Passwords do not match!")
                    return redirect(reverse("admin:change_password"))
        return render(request, "admin/profile.html")
    except Exception as e:
        messages.error(request, e)
        return redirect(reverse("admin:change_password"))

    return render(request, "admin/profile.html")


# Login view
def loginView(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = User.objects.get(username=username)
            if user.check_password(password):
                if user.is_superuser:
                    login(request, user)
                    return redirect(reverse("admin:dashboard"))
                else:
                    messages.error(request, "You need to be an admin to login")
                    return redirect(reverse("admin:login"))
            else:
                messages.error(
                    request, "Account not found. Invalid username or password"
                )
                return redirect(reverse("admin:login"))
        else:
            return render(request, "admin/login.html")
    except Exception as e:
        messages.error(request, e)
        return redirect(reverse("admin:login"))

    return render(request, "admin/login.html")


# Logout view
def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse("admin:login"))
    else:
        return redirect(reverse("admin:not_logged_in"))


def notLoggedIn(request):
    return render(request, "admin/notLoggedIn.html")


def check_updates(request):
    # Get the update status from the shared variable
    has_updates_value = has_updates

    # Reset the update status to False after checking
    has_updates = False

    return JsonResponse({'has_updates': has_updates_value})