from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.contrib.auth.decorators import login_required
from django.urls import  reverse, reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView
from .models import Wallet
from .forms import WalletForm, CategoryForm, TicketForm
# from .models import *


class WalletsView(LoginRequiredMixin,ListView):
    model = Wallet


class AddWalletView(LoginRequiredMixin,CreateView):
    form_class = WalletForm
    template_name = 'tracker/add_wallet.html'

    def get_success_url(self):
        return reverse_lazy('tracker:wallets')

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super(AddWalletView, self).form_valid(form)


class EditWalletView(LoginRequiredMixin,UpdateView):
    model = Wallet
    form_class = WalletForm
    template_name = 'tracker/edit_wallet.html'

class DeleteWalletView(LoginRequiredMixin,DeleteView):
    model = Wallet
    def get_success_url(self):
        return reverse_lazy('tracker:wallets')



@login_required()
def wallet(request,slug):
    wallet = get_object_or_404(Wallet, slug=slug)
    categories = wallet.category_set.all()
    form = TicketForm(wallet,request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            myform = form.save(commit=False)
            myform.wallet = wallet
            myform.save()
            return redirect(reverse(viewname='tracker:wallet', kwargs={'slug':wallet.slug}))
    
    context = {'wallet':wallet, 'categories':categories, 'form':form}
    return render(request, 'tracker/wallet.html',context)



class AddCategoryView(CreateView):
    template_name = 'tracker/add_category.html'
    form_class = CategoryForm
    success_message = 'Success: Category was addded.'
    success_url = reverse_lazy(viewname='tracker:wallets')
    # success_url = reverse_lazy(viewname='tracker:wallet', kwargs={'slug':self.form.instance.wallet})




@login_required()
def stats(request):
    return render(request, template_name='tracker/stats.html')

@login_required()
def tickets(request):
    return render(request, template_name='tracker/tickets.html')

@login_required()
def wallets(request):
    return render(request, template_name='tracker/wallet.html')