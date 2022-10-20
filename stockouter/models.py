from django.db import models

# Create your models here.
class Stock(models.Model):
    ticket=models.CharField(max_length=256,unique=True)
    name=models.CharField(max_length=256)
    price=models.FloatField(null=True)
    pe=models.FloatField(null=True)
    ps=models.FloatField(null=True)
    pb=models.FloatField(null=True)
    ebitda=models.FloatField(null=True)
    env=models.FloatField(null=True)
    net_worth=models.FloatField(null=True)
    roe=models.FloatField(null=True)
    debt_eq=models.FloatField(null=True)
    roa=models.FloatField(null=True)
    roi=models.FloatField(null=True)
    last_divident=models.FloatField(null=True)

class Financial(models.Model):
     revenue=models.FloatField(null=True)
     gross_profit=models.FloatField(null=True)
     income_after_taxes=models.FloatField(null=True)
     net_income=models.FloatField(null=True)
     debt=models.FloatField(null=True)
     stock=models.ForeignKey(Stock,on_delete=models.CASCADE)

class SomeModel(models.Model):
    field1=models.CharField(max_length=256,null=True)
    field2=models.CharField(max_length=256,null=True)
