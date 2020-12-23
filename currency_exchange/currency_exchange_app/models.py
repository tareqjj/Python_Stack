from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=45)


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    mobile_num = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name="categories", on_delete= models.CASCADE)


class Rate(models.Model):
    USD = models.FloatField()
    EUR = models.FloatField()
    GBP = models.FloatField()
    JPY = models.FloatField()
    crated_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class HistoricalData(models.Model):
    timestamp = models.DateTimeField()
    rate_usd = models.FloatField()
    rate_gbp = models.FloatField()
    rate_jpy = models.FloatField()
    rate_eur = models.FloatField()
    rate_jod = models.FloatField()



class Transaction(models.Model):
    fromC = models.CharField(max_length=3)
    toC = models.CharField(max_length=3)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="users", on_delete= models.CASCADE)
    rate = models.ForeignKey(Rate, related_name="rates", on_delete= models.CASCADE)

