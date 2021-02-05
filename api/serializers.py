from rest_framework import serializers
from tracker.models import Wallet, Ticket, Category

class WalletsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['owner','name','balance']


# class UserWalletForeignKey(serializers.PrimaryKeyRelatedField):
#     def get_queryset(self):
#         return Wallet.objects.filter(owner=self.context['user'])

# class TicketsSerialzer(serializers.HyperlinkedModelSerializer):
#     wallet = UserWalletForeignKey()
#     class Meta:
#         model = Ticket
#         fields = ['wallet','value','kind','category','date','title','desc']


# class TicketsSerialzer(serializers.ModelSerializer):
#     # wallet = serializers.PrimaryKeyRelatedField(many=True)
#     class Meta:
#         model = Ticket
#         # fields = ['wallet','value','kind','category','date','title','desc']
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(TicketsSerialzer, self).__init__(*args, **kwargs)
#         user = self.context['user']
#         self.fields['wallet'] = serializers.ChoiceField(choices=Ticket.objects.filter(owner=user))