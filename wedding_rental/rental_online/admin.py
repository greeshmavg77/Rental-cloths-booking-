from django.contrib import admin
from .models import Order, Order_Tbl, cart_Tbl, login_Tbl, product_Tbl, reg_Tbl,Contact

# Register your models here.
admin.site.register(reg_Tbl)
admin.site.register(login_Tbl)
admin.site.register(product_Tbl)
admin.site.register(cart_Tbl)
admin.site.register(Order_Tbl)
admin.site.register(Order)
admin.site.register(Contact)