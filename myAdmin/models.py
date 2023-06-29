from django.db import models
import string
import random
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    expiration_time = models.DateTimeField()

    def generate_code(self):
        characters = string.ascii_letters + string.digits
        code = "".join(random.choices(characters, k=15))
        self.code = code

    def save(self, *args, **kwargs):
        if not self.code:
            self.generate_code()
        if not self.pk:
            self.expiration_time = timezone.now() + timedelta(minutes=15)
        super().save(*args, **kwargs)
