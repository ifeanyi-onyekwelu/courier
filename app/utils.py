from django.contrib import messages
import os
from django.shortcuts import redirect, reverse


# Check if all values passed in are not blank
def checkValues(request, *values):
    if not values:
        messages.error(request, "All fields are reqired")
        return redirect(reverse("app:home_page"))


def get_package_recieved_content(name):
    filepath = os.path.join(
        os.path.dirname(__file__), "..", "templates", "email", "dispatchRecieved.txt"
    )
    with open(filepath, "r") as f:
        content = f.read()
        content = content.replace("{senderName}", name)
    return content
