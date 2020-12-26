from django.db import models
import bcrypt
import datetime
from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_date
import re
# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "first_name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "last_name should be at least 2 characters"
        if len(postData['pw']) < 8:
            errors["password"] = "password should be at least 8 characters"
        if postData['pw'] != postData['pw_cn']:
            errors["pw"] = "password should match"
        if postData['birth_date'] > str(timezone.now()):
            errors["desc"] = "The birth date should be in the past!"
        if User.objects.filter(email=postData['email']):
            errors['not_unique'] = 'This Email is already registered'
        # if (datetime.date.today() - parse_date(postData['birth_date'])).days < 4745:
        #     errors['COPPA'] = 'This Application is not suitable for kids'
        return errors

    def login_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(User.objects.filter(email=postData['email'])) == 0:
            errors['not_registered'] = "You need to Register"
        if len(postData['pw']) < 8:
            errors["password"] = "password should be at least 8 characters"
        return errors


class CardManager(models.Manager):
    def card_validator(self, CardInfo):
        errors = {}
        EMAIL_REGEX = re.compile(r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$')
        if not EMAIL_REGEX.match(CardInfo['card_number']):
            errors['CardNumber'] = "Invalid Card Number!"
        if str(timezone.now()) > CardInfo['expire']:
            errors['COPPA'] = 'This Debit Card is Expired'
        return errors


class Category(models.Model):
    name = models.CharField(max_length=45)


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    # mobile_num = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    # type = models.BinaryField(default=0)
    # logged = models.BinaryField(default=0)
    # category = models.ForeignKey(Category, related_name="categories", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()


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
    rate = models.ForeignKey(Rate, related_name="rates", on_delete=models.CASCADE)


def Transfer(Payment_Info, user_id):
    hash_DCN = bcrypt.hashpw(Payment_Info['card_number'].encode(), bcrypt.gensalt()).decode()
    hash_cvv = bcrypt.hashpw(Payment_Info['cvv'].encode(), bcrypt.gensalt()).decode()
    PaymentInfo.objects.create(userName=Payment_Info['user_name'], user=User.objects.get(id=user_id), debitCardHash=hash_DCN, cvv_hash=hash_cvv)
    Transaction.objects.create(fromC=Payment_Info['from'], fromU=User.objects.get(id=user_id), toC=Payment_Info['to'], amount=Payment_Info['amount'], rate=Rate.objects.latest('timestamp'))


def registration(new_user):
    hash_pw = bcrypt.hashpw(new_user['pw'].encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(first_name=new_user['first_name'], last_name=new_user['last_name'],
                               email=new_user['email'], birth_date=new_user['birth_date'], password=hash_pw)
    return user.id


def log_in(log_in_data):
    user = User.objects.filter(email=log_in_data['email'])
    if bcrypt.checkpw(log_in_data['pw'].encode(), user[0].password.encode()):
        context= {
            'flag': True,
            'this_user': user[0]
        }
        return context
    else:
        context = {
            'flag': False
        }
        return context