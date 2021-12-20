from django.db import models

# Create your models here.
class Stock(models.Model):
    ticket=models.CharField(max_length=256,unique=True)
    name=models.CharField(max_length=256)
    price=models.IntegerField(null=True)
    pe=models.IntegerField(null=True)
    ps=models.IntegerField(null=True)
    pb=models.IntegerField(null=True)
    ebitda=models.IntegerField(null=True)
    env=models.IntegerField(null=True)
    net_worth=models.IntegerField(null=True)
    roe=models.IntegerField(null=True)
    debt_eq=models.IntegerField(null=True)
    roa=models.IntegerField(null=True)
    roi=models.IntegerField(null=True)
    last_divident=models.IntegerField(null=True)

class Financial(models.Model):
     revenue=models.IntegerField(null=True)
     gross_profit=models.IntegerField(null=True)
     income_after_taxes=models.IntegerField(null=True)
     net_income=models.IntegerField(null=True)
     debt=models.IntegerField(null=True)
     stock=models.ForeignKey(Stock,on_delete=models.CASCADE)
