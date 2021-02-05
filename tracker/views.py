from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.contrib.auth.decorators import login_required
from django.urls import  reverse, reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from django.db.models import Q
from .models import Wallet, Ticket
from .forms import WalletForm, CategoryForm, TicketForm
# from .models import *


class WalletsView(LoginRequiredMixin,ListView):
    model = Wallet
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


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
    wallet = get_object_or_404(Wallet, slug=slug,owner=request.user)
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

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddCategoryView,self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs
    # success_url = reverse_lazy(viewname='tracker:wallet', kwargs={'slug':self.form.instance.wallet})


# def search_ajax(request):
#     if request.method == "POST":
#         data = json.loads(request.body).get('searchText')


@login_required()
def stats(request):
    return render(request, template_name='tracker/stats.html')
    user_tickets = Ticket.objects.filter(wallet__owner=request.user)

@login_required()
def tickets(request,slug):
    context = {}
    return render(request, template_name='tracker/tickets.html', context=context)


@login_required()
def wallettickets(request,slug):
    wallet = get_object_or_404(Wallet,slug=slug, owner=request.user)
    tickets = Ticket.objects.filter(wallet=wallet)
    paginator = Paginator(tickets, 8)
    page_number = request.GET.get('page')
    page_tickets = paginator.get_page(page_number)
    context = {'tickets':tickets, 'wallet':wallet, 'page_tickets':page_tickets}
    return render(request, template_name='tracker/tickets.html', context=context)


@login_required()
def ajax_search(request):
    if request.method == "POST":
        search_text = request.POST.get('searchText')
        wallet = request.POST.get('wallet')
        my_tickets = Ticket.objects.filter(wallet__owner=request.user,wallet__name=wallet)
        results = my_tickets.filter(Q(title__icontains=search_text)
            |Q(desc__icontains=search_text)|Q(category__name__icontains=search_text))
        data = list(results.values())
        return JsonResponse(data, safe=False)

@login_required()
def wallets(request):
    return render(request, template_name='tracker/wallet.html')