# from django.db.models.signals import pre_delete, post_delete
# from django.dispatch import receiver
# from .models import Ticket, Wallet

# @receiver(pre_delete, sender=Ticket)
# def wallet_balance_upadate_with_ticket_delete(sender, instance, **kwargs):
#     print(kwargs)
#     # ticket = 
#     wallet = instance.wallet
#     print(wallet)
#     # ticket_value = instance.value
#     # wallet.balance = wallet.balance-ticket_value
#     # wallet.save()
