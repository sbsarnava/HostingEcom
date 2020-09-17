from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import BillingAddress, Order, CompletedOrder


@receiver(post_save, sender=Order)
def dont_save_if_all_fields_matching(sender, instance, created, **kwargs):
    if not created:
        currentOrder = instance
        previousBilling = BillingAddress.objects.filter(user=currentOrder.user,
                                                        firstname=currentOrder.billingAddress.firstname,
                                                        lastname=currentOrder.billingAddress.lastname,
                                                        phonenumber=currentOrder.billingAddress.phonenumber,
                                                        address1=currentOrder.billingAddress.address1,
                                                        address2=currentOrder.billingAddress.address2,
                                                        city=currentOrder.billingAddress.city,
                                                        country=currentOrder.billingAddress.country,
                                                        state=currentOrder.billingAddress.state,
                                                        pincode=currentOrder.billingAddress.pincode
                                                        )
        currentBilling = currentOrder.billingAddress
        if len(previousBilling) > 1:
            currentOrder.billingAddress = previousBilling[0]
            currentBilling.delete()


@receiver(post_save, sender=Order)
def convert_to_completed_order(sender, instance, created, **kwargs):
    if not created:
        if instance.paymentSuccessful == True:
            CompletedOrder.objects.create(user=instance.user, completedOrder=instance)


@receiver(post_save, sender=CompletedOrder)
def process_order(sender, instance, created, **kwargs):
    for item in instance.completedOrder.cartItems.item.all():
        print(item.item.title)
