from django.contrib import admin

# Register your models here.
from . models import homepage,products,Category,Customers,Order
class AdminProduct(admin.ModelAdmin):
    list_display = ['name','desc','product_image','categories','id']

class AdminCategory(admin.ModelAdmin):
    list_display = ['catname','id']

admin.site.register(homepage)
admin.site.register(products,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(Customers)
admin.site.register(Order)