from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import  reverse
from django.utils.text import slugify


class Wallet(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True,null=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self,*args,**kwargs):
        if self.name:     
            self.slug = slugify(self.name)
        super(Wallet,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse(viewname='tracker:wallet', kwargs={'slug':self.slug})


    def __str__(self):
        return self.name


class Category(models.Model):
    wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True,null=True)

    class Meta:
        verbose_name_plural = 'Categories'


    def save(self,*args,**kwargs):
        if self.name:     
            self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)
        
    def __str__(self):
        return self.name


CHOICES = (('in','Income'),('out','Expenses'))
class Ticket(models.Model):
    wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE, related_name='tickets')
    value = models.DecimalField(max_digits=15, decimal_places=2)
    kind = models.CharField(max_length=20, choices=CHOICES)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=50, default="No Title")
    desc = models.TextField(default='')

    class Meta:
        ordering =('-date',)

    def save(self,*args,**kwargs):
        if self.kind == 'in':
            self.wallet.balance += self.value
        elif self.kind == 'out':
            self.wallet.balance -= self.value            
        wallet = Wallet.objects.get(id=self.wallet.id)
        wallet.balance = self.wallet.balance
        wallet.save()
        super(Ticket, self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.title}-{self.value}"

