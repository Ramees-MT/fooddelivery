from django.contrib import admin
from .models import Registration,Login,Cart,Wishlist,Placeorder,Foodcategory,Fooditems
# Register your models here.
admin.site.register(Registration)
admin.site.register(Login)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Placeorder)
admin.site.register(Fooditems)

admin.site.register(Foodcategory)



