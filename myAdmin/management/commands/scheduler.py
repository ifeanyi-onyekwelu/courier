from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.utils import timezone
import logging
from myAdmin.models import Coupon

# Variable to track the update status
has_updates = False

class Command(BaseCommand):
    help = 'Runs the scheduler.'

    def handle(self, *args, **options):
        def update_coupon_statuses():
            print("Updating coupon statuses...")
            # Get expired coupons
            expired_coupons = Coupon.objects.filter(expiration_time__lte=timezone.now())
            # Update coupon statuses
            for coupon in expired_coupons:
                coupon.is_expired = True
                coupon.save()

            logging.info("Coupon status update executed.")

            # Set the update status to True
            global has_updates
            has_updates = True
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)

        # Create a scheduler instance
        scheduler = BackgroundScheduler()

        # Schedule the task to run every minute
        scheduler.add_job(update_coupon_statuses, IntervalTrigger(minutes=1))

        # Start the scheduler
        scheduler.start()

        logging.info("Scheduler started.")