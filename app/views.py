from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from . import utils
from .models import Package
from myAdmin.models import Coupon
import os


def home(request):
    return render(request, "index.html")

# handle dispatch package
def dispatchPackage(request):
    try:
        if request.method == "POST":
            senderName = request.POST.get("senderName")
            senderEmail = request.POST.get("senderEmail")
            senderPhone = request.POST.get("senderPhone")
            senderAddress = request.POST.get("senderAddress")
            recipientName = request.POST.get("recipientName")
            recipientPhone = request.POST.get("recipientPhone")
            recipientAddress = request.POST.get("recipientAddress")
            product = request.POST.get("product")
            weight = request.POST.get("weight")
            height = request.POST.get("height")
            coupon = request.POST.get("coupon")
            delivery_location = request.POST.get("additionalDetails")
            additionalComment = request.POST.get("deliveryLocation")
            # Make neccessary validation
            utils.checkValues(
                request,
                senderName,
                senderEmail,
                senderAddress,
                senderPhone,
                senderPhone,
                recipientName,
                coupon,
                recipientPhone,
                recipientAddress,
                product,
                weight,
                height,
                delivery_location,
                additionalComment,
            )

            couponCode = Coupon.objects.get(code=coupon)

            if couponCode is not None:
                print("Coupon code exists")
                if couponCode.is_expired == True:
                    print("Code has expired fam")
                    return JsonResponse({"message": "expired"})
                elif couponCode.is_used == True:
                    print("Code has been used fam")
                    return JsonResponse({"message": "used"})

                newDelivery = Package.objects.create(
                    senderName=senderName,
                    senderEmail=senderEmail,
                    senderPhone=senderPhone,
                    senderAddress=senderAddress,
                    recipeintName=recipientName,
                    recipeintAddress=recipientAddress,
                    recipeintPhone=recipientPhone,
                    product=product,
                    weight=weight,
                    height=height,
                    coupon=coupon,
                    additionalComment=additionalComment,
                    delivery_location=delivery_location,
                )
                messages.success(
                    request,
                    "Your package has been dispatched. You will recieve an email when your parcel is out for packaging.",
                )
                trackingId = newDelivery.tracking_id

                email_subject = "Parcel registered"
                email_body = utils.get_package_recieved_content(senderName)
                send_mail(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [senderEmail],
                    fail_silently=False,
                )

                # Store a new trackingId in the session
                request.session["trackingId"] = trackingId
                request.session.save()
                couponCode.is_used = True
                couponCode.save()
                redirect_url = reverse("app:home_page")
                return JsonResponse(
                    {"message": "created", "tracking_id": trackingId}
                )
            else:
                messages.error(request, "Code is invalid")
                return JsonResponse({"message": "invalid"})
    except Exception as e:
        print(e)
        return redirect(reverse("app:home_page"))
    return render(request, "index.html")

# Get the current created package info
def get_package_info(request):
    if request.method == "GET":
        tracking_id = request.GET.get("trackingId")
        # Retrieve the package from the database
        try:
            package = Package.objects.get(tracking_id=tracking_id)
            package_info = {
                "trackingId": package.tracking_id
            }
            return JsonResponse(package_info)
        except Package.DoesNotExist:
            return JsonResponse({"error": "Package not found"})

    return JsonResponse({"error": "Invalid request method"})

# handle track package
def trackPackage(request):
    try:
        if request.method == "POST":
            trackingId = request.POST.get("trackingID")
            package = Package.objects.filter(tracking_id=trackingId).first()

            if package is not None:
                request.session["trackingId"] = trackingId
                return JsonResponse({"message": "success"})
            else:
                return JsonResponse({"message": "notFound"})
            
    except Exception as e:
        messages.error(request, str(e))
    return render(request, "index.html")

def view_package_status(request):
    trackingId = request.session.get("trackingId")
    package = Package.objects.filter(tracking_id=trackingId).first()
    context = {
        'package': package
    }
    
    return render(request, 'status.html', context)

# Handle contact us form actions
def sendMessage(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        try:
            send_mail(
                name,
                message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return JsonResponse({"message": 'success'})
        except Exception as e:
            return JsonResponse({"message": 'unsuccessful', "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method."})