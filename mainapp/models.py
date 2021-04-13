import datetime
from unicodedata import category
from django.db import models

# Create your models here.
class homepage(models.Model):
    title=models.CharField(max_length=100)
    desc=models.CharField(max_length=300)
    img=models.ImageField(upload_to='mainapp/images')


class Category(models.Model):
    catname=models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    def __str__(self):
        return self.catname

class products(models.Model):
    name=models.CharField(max_length=100)
    desc=models.CharField(max_length=300)
    description=models.CharField(max_length=400,default=1)
    product_image=models.ImageField(upload_to='mainapp/images')
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.name

    @staticmethod
    def get_products_by_id(ids):
        return products.objects.filter(id__in=ids)
    @staticmethod
    def get_all_product():
        return products.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):

        if category_id:
            return products.objects.filter(categories = category_id)
        else:
            return products.get_all_product()

class Customers(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    password=models.CharField(max_length=300)
    def __str__(self):
        return self.first_name
    def register(self):
        self.save()
    @staticmethod
    def get_customer_by_phone(phone):
        try:
            return Customers.objects.get(phone=phone)
        except:
            return False


class Order(models.Model):
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customers,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    address=models.CharField(max_length=200,default="",blank=True)
    phone=models.CharField(max_length=15,default="",blank=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)
    mode=models.CharField(max_length=20,default="",blank=True)

    def placeOrder(self):
        self.save()

    @staticmethod

    def get_orders_by_customer(customer_id):
        return Order\
            .objects\
            .filter(customer=customer_id)\
            .order_by('-date')