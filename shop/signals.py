# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from .models import BillingAddress
#
#
# @receiver(post_save, sender=BillingAddress)
# def dont_save_if_all_fields_matching(sender, instance, created, **kwargs):
#     if created:
#         previousBilling = BillingAddress.objects.all()
#         print('From the Signal: ')
#         print(instance.id)
#         range1 = 10
#         range2 = len(previousBilling)
#         match = [[False] * range1] * range2
#         c1 = 0
#         for i in range(len(previousBilling)):
#             if previousBilling[i].firstname == instance.firstname:
#                 match[c1][0] = True
#             if previousBilling[i].lastname == instance.lastname:
#                 match[c1][1] = True
#             if previousBilling[i].phonenumber == instance.phonenumber:
#                 match[c1][2] = True
#             if previousBilling[i].email == instance.email:
#                 match[c1][3] = True
#             if previousBilling[i].address1 == instance.address1:
#                 match[c1][4] = True
#             if previousBilling[i].address2 == instance.address2:
#                 match[c1][5] = True
#             if previousBilling[i].city == instance.city:
#                 match[c1][6] = True
#             if previousBilling[i].country == instance.country:
#                 match[c1][7] = True
#             if previousBilling[i].state == instance.state:
#                 match[c1][8] = True
#             if previousBilling[i].pincode == instance.pincode:
#                 match[c1][9] = True
#             c1 += 1
#         print('Match:')
#         print(match)
#         sort = [True] * len(match)
#
#         for i in range(len(match)):
#             for j in range(len(match[i])):
#                 if match[i][j] == False:
#                     sort[i] = False
#                 else:
#                     continue
#         print('Sort:')
#         print(sort)
#         for i in range(len(sort)):
#             if i == True:
#                 # relatedOrder = currentBilling.order
#                 # relatedOrder.billingAddress = BillingAddress.objects.get(id=i)
#                 # relatedOrder.save()
#                 # currentBilling.delete()
#                 relatedOrder = instance.order_set.get(billingAddress=instance)
#                 currentBilling.order_set.clear()
#                 relatedOrder.billingAddress_id = i
#                 relatedOrder.save()
#                 instance.delete()
#                 return
