from django.db import models
import json
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from datetime import datetime

class Vendor(models.Model):
	name = models.CharField(max_length=100)
	contact_details = models.TextField()
	address = models.TextField()
	vendor_code = models.CharField(max_length=50, unique=True)
	on_time_delivery_rate = models.FloatField()
	quality_rating_avg = models.FloatField()
	average_response_time = models.FloatField()
	fulfillment_rate = models.FloatField()

	def __str__(self):
		return self.name
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('canceled', 'canceled')
    ]

    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            return

        previous_order = PurchaseOrder.objects.get(pk=self.pk)
        super().save(*args, **kwargs)

        vendor = self.vendor
        total_orders = PurchaseOrder.objects.filter(vendor=vendor)
        completed_orders = total_orders.filter(status='completed')
        performance = HistoricalPerformance.objects.filter(vendor=vendor).last()

        if self.status == 'completed' and previous_order.status != 'completed':
            if not self.quality_rating:
                if not vendor.quality_rating_avg:
                    vendor.quality_rating_avg = 0
            else:
                vendor.quality_rating_avg = calculate_quality_rating_avg(completed_orders)

            vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(completed_orders)
            vendor.average_response_time = calculate_average_response_time(total_orders)
            vendor.fulfillment_rate = calculate_fulfillment_rate(completed_orders)

            vendor.save()

            HistoricalPerformance.objects.create(
                vendor=vendor,
                date=datetime.now(),
                on_time_delivery_rate=vendor.on_time_delivery_rate,
                quality_rating_avg=vendor.quality_rating_avg,
                average_response_time=vendor.average_response_time,
                fulfillment_rate=vendor.fulfillment_rate
            )
        elif self.status == 'completed' and self.quality_rating and self.quality_rating != previous_order.quality_rating:
            vendor.quality_rating_avg = calculate_quality_rating_avg(completed_orders)
            vendor.save()
            if performance:
                performance.quality_rating_avg = vendor.quality_rating_avg
                performance.save()
        elif self.acknowledgment_date != previous_order.acknowledgment_date:
            vendor.average_response_time = calculate_average_response_time(total_orders)
            vendor.save()
            if performance:
                performance.average_response_time = vendor.average_response_time
                performance.save()
        elif self.status != previous_order.status:
            vendor.fulfillment_rate = calculate_fulfillment_rate(completed_orders)
            vendor.save()
            if performance:
                performance.fulfillment_rate = vendor.fulfillment_rate
                performance.save()


class HistoricalPerformance(models.Model):
	vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
	date = models.DateTimeField()
	on_time_delivery_rate = models.FloatField()
	quality_rating_avg = models.FloatField()
	average_response_time = models.FloatField()
	fulfillment_rate = models.FloatField()


def calculate_on_time_delivery_rate(orders):
    if orders.exists():
        return (orders.filter(issue_date__lte=models.F('delivery_date')).count() / orders.count()) * 100
    return 0

def calculate_quality_rating_avg(orders):
    if orders.exists():
        return orders.exclude(quality_rating=None).aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating']
    return 0

def calculate_average_response_time(orders):
    if orders.exists():
        total_time = sum((order.acknowledgment_date - order.issue_date).total_seconds() for order in orders if order.acknowledgment_date)
        return total_time / orders.count()
    return 0

def calculate_fulfillment_rate(orders):
    if orders.exists():
        return (orders.filter(status='completed').count() / orders.count()) * 100
    return 0
