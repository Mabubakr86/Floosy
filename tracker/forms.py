from django import forms
from .models import *
from tempus_dominus.widgets import DateTimePicker
from bootstrap_modal_forms.forms import BSModalModelForm


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name','balance']



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['wallet','name']      

class TicketForm(forms.ModelForm):
    def __init__(self, wallet, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(wallet=wallet)
        
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':''}))
    date = forms.DateTimeField(widget=DateTimePicker(options={'useCurrent': True,'collapse': True,}
        ,attrs={'append': 'fa fa-calendar','icon_toggle': True,}),) 
    desc = forms.CharField(widget=forms.Textarea(attrs={'cols':4,'rows':4}), required=False)   
    class Meta:
        model = Ticket
        exclude = ['wallet',]
