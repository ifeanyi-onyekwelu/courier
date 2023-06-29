from django.db import models
import random
import uuid
import string


class Package(models.Model):
    STATUS = (
        ("Processing", "Processing"),
        ("Packaging", "Packaging"),
        ("In Transit", "In Transit"),
        ("Shipping", "Shipping"),
        ("Delivered", "Delivered"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    senderName = models.CharField(max_length=255, default="")
    senderEmail = models.CharField(max_length=255, default="")
    senderPhone = models.CharField(max_length=255, default="")
    senderAddress = models.CharField(max_length=255, default="")
    recipeintName = models.CharField(max_length=255, default="")
    recipeintPhone = models.CharField(max_length=255, default="")
    recipeintAddress = models.CharField(max_length=255, default="")
    product = models.CharField(max_length=255)
    tracking_id = models.CharField(max_length=10)
    weight = models.DecimalField(decimal_places=2, max_digits=100)
    height = models.DecimalField(decimal_places=2, max_digits=100)
    coupon = models.CharField(max_length=15, default="")
    delivery_location = models.CharField(max_length=255)
    additionalComment = models.CharField(max_length=1000)
    status = models.CharField(max_length=255, choices=STATUS, default="Processing")
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_tracking_id(self):
        characters = string.ascii_letters + string.digits
        tracking_id = "".join(random.choices(characters, k=15))
        self.tracking_id = tracking_id

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.generate_tracking_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.senderName} - TO - {self.recipeintName} -- {self.status}"
