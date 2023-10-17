from store.signals import order_created
from django.dispatch import receiver


#Create Signal for New User
#This function will call once user model save

@receiver(order_created)
def on_order_created(sender, **kwargs):
    print(kwargs['order'])
