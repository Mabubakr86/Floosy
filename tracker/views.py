from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.contrib.auth.decorators import login_required
from django.urls import  reverse, reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Sum
import json
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta, time
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

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

class DeleteWalletView(LoginRequiredMixin,DeleteView):
    model = Wallet
    def get_success_url(self):
        return reverse_lazy('tracker:wallets')

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)



@login_required()
def wallet(request,slug):
    cat_list = False
    tickets_count = None
    wallet = get_object_or_404(Wallet, slug=slug,owner=request.user)
    categories = wallet.category_set.all()
    if categories.count() > 0:
        cat_list = True
    tickets = wallet.tickets.filter(kind='out')
    if tickets.count() > 0:
        tickets_count = tickets.count()
    data = {}
    for ticket in tickets:
        cat_name = ticket.category.name
        if not (cat_name in data.keys()): 
            data[cat_name]=float(ticket.value)
        else:
            data[cat_name]= data[cat_name]+float(ticket.value)

    form = TicketForm(wallet,request.POST or None)


    if request.method == "POST":
        if form.is_valid():
            myform = form.save(commit=False)
            myform.wallet = wallet
            myform.save()
            return redirect(reverse(viewname='tracker:wallet', kwargs={'slug':wallet.slug}))

    context = {'wallet':wallet, 'categories':categories, 'form':form
    , 'data':data, 'tickets_count': tickets_count,'cat_list':cat_list}
    return render(request, 'tracker/wallet.html',context)


class AddCategoryView(LoginRequiredMixin,CreateView):
    template_name = 'tracker/add_category.html'
    form_class = CategoryForm
    success_message = 'Success: Category was addded.'
    success_url = reverse_lazy(viewname='tracker:wallets')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddCategoryView,self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs
    # success_url = reverse_lazy(viewname='tracker:wallet', kwargs={'slug':self.form.instance.wallet})


@login_required()
def stats(request, slug):
    # Set initial values:
    expense = False
    income = False
    graph = False

    expenses_total = "No Matching Data"
    max_expense_date = False
    max_expense_value = "No Matching Data"
    categories_expenses = "No Matching Data"
    expenses_log = "No Matching Data"


    income_total = "No Matching Data"
    max_income_date = False
    max_income_value = "No Matching Data"
    categories_incomes = "NNo Matching Data"
    incomes_log = "No Matching Data"



    # Get start of Week, Month, and Year
    today = datetime.today()
    today_temp = today.date().strftime("%Y-%m-%d")
    week_start = today-timedelta(days=today.weekday())
    month_start = today-timedelta(days=today.day)
    year_start = today-timedelta(weeks=today.isocalendar()[1])
    # Get the proper tickets
    wallet = get_object_or_404(Wallet, slug=slug,owner=request.user)
    categories = wallet.category_set.all()
    expense_tickets = wallet.tickets.filter(kind='out')
    income_tickets = wallet.tickets.filter(kind='in')
    # start to populate context
    week_sum = expense_tickets.filter(Q(date__gte=week_start)&
        Q(date__lte=timezone.now())).aggregate(week_sum=Sum('value'))['week_sum']
    month_sum = expense_tickets.filter(Q(date__gte=month_start)&
        Q(date__lte=timezone.now())).aggregate(month_sum=Sum('value'))['month_sum']
    year_sum = expense_tickets.filter(Q(date__gte=year_start)&
        Q(date__lte=timezone.now())).aggregate(year_sum=Sum('value'))['year_sum']

    if week_sum:
        week_sum = float(week_sum)
    if month_sum:
        month_sum = float(month_sum)
    if year_sum:
        year_sum = float(year_sum)

    if request.method == 'POST':
        from_ = request.POST.get('from')
        to = request.POST.get('to')
        kind = request.POST.get('kind')

        if to < from_ or kind=='Choose...':
            messages.error(request,'End date is before start date, or no kind selection')
            return redirect(reverse('tracker:stats', kwargs={'slug': slug}))
        from_ = datetime.strptime(from_, "%Y-%m-%d")
        to = datetime.strptime(to, "%Y-%m-%d")

        # Dealing with expenses:
        if kind == 'Expenses':
            expense = True
            expenses = expense_tickets.filter(Q(date__gte=from_)&Q(date__lte=to))
            expenses_total_ = expenses.aggregate(total=Sum('value'))['total']
            print(expenses_total_)
            print(expenses)
            if expenses_total_ and expenses:
                graph = True
                expenses_total = float(expenses_total_)
                max_card = expenses.order_by('-value').first()
                max_expense_date = max_card.date
                max_expense_value = float(max_card.value)
                print(max_expense_date)

                # Polpulate Categories chart
                categories_expenses = {}
                for ticket in expenses:
                    cat_name = ticket.category.name
                    if not (cat_name in categories_expenses.keys()):
                        categories_expenses[cat_name]=float(ticket.value)
                    else:
                        categories_expenses[cat_name]= categories_expenses[cat_name]+float(ticket.value)
                # Populate Date Chart
                repeated_dates = []
                expenses_log =[]
                for ticket in expenses:
                    t = {}
                    value = ticket.value
                    date = ticket.date
                    date = str(date.date())
                    # to sum up tickets with the same date
                    if date not in repeated_dates:
                        t['date'] = str(date)
                        t['y'] = float(value)
                        repeated_dates.append(date)
                        expenses_log.append(t)
                    else:
                        for card in expenses_log:
                            if date == card['date']:
                                last_value = card['y']
                                card['y'] = last_value + float(value)
                expenses_log = json.dumps(expenses_log)

        # if selected Income
        elif kind == 'Income':
            income = True
            incomes = income_tickets.filter(Q(date__gte=from_)&Q(date__lte=to))
            income_total = incomes.aggregate(total=Sum('value'))['total']
            if income_total and incomes:
                graph = True

                income_total = float(income_total)
                max_card = incomes.order_by('-value').first()
                max_income_date = max_card.date
                max_income_value = float(max_card.value)

                # Polpulate Categories chart
                categories_incomes = {}
                for ticket in incomes:
                    cat_name = ticket.category.name
                    if not (cat_name in categories_incomes.keys()):
                        categories_incomes[cat_name]=float(ticket.value)
                    else:
                        categories_incomes[cat_name]= categories_incomes[cat_name]+float(ticket.value)


                # Populate Date Chart
                repeated_dates = []
                incomes_log =[]
                for ticket in incomes:
                    t = {}
                    value = ticket.value
                    date = ticket.date
                    date = str(date.date())
                    # to sum up tickets with the same date
                    if date not in repeated_dates:
                        t['date'] = str(date)
                        t['y'] = float(value)
                        repeated_dates.append(date)
                        incomes_log.append(t)
                    else:
                        for card in incomes_log:
                            if date == card['date']:
                                last_value = card['y']
                                card['y'] = last_value + float(value)
                incomes_log = json.dumps(incomes_log)


        redirect(reverse('tracker:stats',kwargs={'slug':slug}))

    context = {'expense':expense,'week_sum':week_sum,
    'month_sum':month_sum,'year_sum':year_sum,'expenses_total':expenses_total,
    'max_expense_date':max_expense_date,'max_expense_value':max_expense_value,
    'categories_expenses': categories_expenses,'expenses_log':expenses_log,'income':income,
    'income_total': income_total,'max_income_date': max_income_date, 
    'max_income_value':max_income_value,'categories_incomes': categories_incomes,
    'incomes_log':incomes_log,'today': today_temp,'graph':graph,

    }
    print(today_temp)
    return render(request, template_name='tracker/stats.html', context=context)

@login_required()
def tickets(request,slug):
    context = {}
    return render(request, template_name='tracker/tickets.html', context=context)


@login_required()
def wallettickets(request,slug):
    wallet = get_object_or_404(Wallet,slug=slug, owner=request.user)
    tickets = Ticket.objects.filter(wallet=wallet)
    paginator = Paginator(tickets, 12)
    page_number = request.GET.get('page')
    page_tickets = paginator.get_page(page_number)
    context = {'tickets':tickets, 'wallet':wallet, 'page_tickets':page_tickets}
    return render(request, template_name='tracker/tickets.html', context=context)

@login_required()
def edit_ticket(request,id):
    ticket = get_object_or_404(Ticket,id=id)
    wallet = ticket.wallet
    old_value = ticket.value
    if request.method == 'POST':
        form = TicketForm(wallet, request.POST, instance=ticket )
        if form.is_valid():
            new_value = form.cleaned_data['value']
            diff = new_value-old_value
            wallet.balance = wallet.balance + diff
            wallet.save()
            form.save()
            messages.success(request,'Ticket has been modified')
            return redirect(reverse(viewname='tracker:wallet', kwargs={'slug':wallet.slug}))
    form = TicketForm(wallet,instance=ticket )

    context = {'ticket':ticket, 'form':form, 'wallet':wallet}
    return render(request, 'tracker/edit_ticket.html', context=context)

class TicketDeleteView(LoginRequiredMixin,DeleteView):
    model = Ticket
    def get_success_url(self):
        return reverse(viewname='tracker:wallets')

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