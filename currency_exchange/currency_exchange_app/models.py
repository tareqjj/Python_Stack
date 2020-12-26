from django.db import models
import bcrypt
import datetime
from datetime import datetime
from django.utils.dateparse import parse_date
import re
# Create your models here.


class CardManager(models.Manager):
    def card_validator(self, CardInfo):
        errors = {}
        EMAIL_REGEX = re.compile(r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$')
        if not EMAIL_REGEX.match(CardInfo['email']):
            errors['CardNumber'] = "Invalid Card Number!"
        if (datetime.date.today() - parse_date(CardInfo['birth_date'])).seconds < 0:
            errors['COPPA'] = 'This Credit Debit is Expired'
        return errors


class Category(models.Model):
    name = models.CharField(max_length=45)


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    mobile_num = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=255)
    type = models.BinaryField(default=0)
    logged = models.BinaryField(default=0)
    category = models.ForeignKey(Category, related_name="categories", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Rate(models.Model):
    timestamp = models.DateTimeField(default=datetime.now)
    date = models.DateTimeField()
    USD = models.FloatField()
    JOD = models.FloatField()
    GBP = models.FloatField()
    JPY = models.FloatField()
    ILS = models.FloatField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = datetime.utcnow()
        return super(Rate, self).save(*args, **kwargs)


class HistoricalData(models.Model):
    timestamp = models.DateTimeField()
    rate_usd = models.FloatField()
    rate_gbp = models.FloatField()
    rate_jpy = models.FloatField()
    rate_eur = models.FloatField()
    rate_jod = models.FloatField()


class PaymentInfo(models.Model):
    userName = models.CharField(max_length=45)
    user = models.ForeignKey(User, related_name="fromUsers", on_delete=models.CASCADE)
    debitCardHash = models.CharField(max_length=255)
    cvv_hash = models.CharField(max_length=255)
    objects = CardManager()


class Transaction(models.Model):
    fromC = models.CharField(max_length=3)
    fromU = models.ForeignKey(PaymentInfo, related_name="userTransActions", on_delete=models.CASCADE)
    toC = models.CharField(max_length=3)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)
    rate = models.ForeignKey(Rate, related_name="rates", on_delete=models.CASCADE)


def Transfer(Payment_Info, user_id):
    hash_DCN = bcrypt.hashpw(Payment_Info['card_number'].encode(), bcrypt.gensalt()).decode()
    hash_cvv = bcrypt.hashpw(Payment_Info['cvv'].encode(), bcrypt.gensalt()).decode()
    PaymentInfo.objects.create(userName=Payment_Info['user_name'], user=User.objects.get(id=user_id), debitCardHash=hash_DCN, cvv_hash=hash_cvv)