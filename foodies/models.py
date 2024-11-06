from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Login(models.Model):
  email=models.EmailField()
  password=models.CharField(max_length=20)
  role=models.CharField(max_length=15)



class Registration(models.Model):
  username=models.CharField(max_length=30)
  email=models.EmailField()
  password=models.CharField(max_length=30)
  phone=models.CharField(max_length=30)
  role=models.CharField(max_length=30)
  login_id=models.OneToOneField(Login,on_delete=models.CASCADE)

class Foodcategory(models.Model):
  categoryname=models.CharField(max_length=50)
  categoryimage=models.URLField(max_length=200)


class Fooditems(models.Model):
    itemname = models.CharField(max_length=100)
    itemprice = models.DecimalField(max_digits=10, decimal_places=2)
    itemdescription = models.TextField()
    itemimage = models.URLField(max_length=200)
    itemcategory = models.ForeignKey(Foodcategory, on_delete=models.CASCADE) 


class Review(models.Model):
    itemname=models.CharField(max_length=50)
    itemid=models.CharField(max_length=7)
    username=models.CharField(max_length=50)
    userid=models.CharField(max_length=50)
    itemdescription=models.CharField(max_length=500)

class Cart(models.Model):
   itemname=models.CharField(max_length=50)
   itemid=models.CharField(max_length=7)
   userid=models.CharField(max_length=50)
   quantity=models.IntegerField(default=1)
   cart_status=models.IntegerField(default=1)
   itemprice=models.DecimalField(max_digits=10, decimal_places=2)
   itemimage=models.URLField(max_length=200)


class Wishlist(models.Model):
   itemname=models.CharField(max_length=50)
   itemid=models.CharField(max_length=7)
   userid=models.CharField(max_length=50)
   quantity=models.CharField(max_length=50)
   wishliststatus=models.CharField(max_length=50)
   itemprice=models.DecimalField(max_digits=10, decimal_places=2)
   itemimage=models.ImageField()

class Placeorder(models.Model):
   
   itemname=models.CharField(max_length=50)
   itemid=models.CharField(max_length=7)
   userid=models.CharField(max_length=50)
   quantity=models.CharField(max_length=50)
   cart_status=models.IntegerField(default=1)
   itemprice=models.DecimalField(max_digits=10, decimal_places=2)
   itemimage=models.URLField(max_length=200)
   date=models.DateTimeField(auto_now=True)

class Address(models.Model):
    name=models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    userid=models.ForeignKey(Login,on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)



class Special_offer(models.Model):
   itemname=models.CharField(max_length=50)
   itemimage=models.URLField(max_length=200)
   offerdetails=models.CharField(max_length=200)

class Weekly_special(models.Model):
   specialname=models.CharField(max_length=50)
   specialimage=models.URLField(max_length=200)








