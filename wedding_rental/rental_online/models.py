# from datetime import timezone
from django.db import models

# user interface

# register

class reg_Tbl(models.Model):
    name=models.CharField(max_length=50)
    mobile=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=50)
    confirm_password=models.CharField(max_length=50)
    user_type=models.CharField(max_length=50,default='user')
    
    def __str__(self):
        return self.name
    
# login  
class login_Tbl(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=50)

# product
class product_Tbl(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unisex', 'Unisex'),
    ]

    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    item_name=models.CharField(max_length=50)
    item_image=models.FileField(upload_to='pictures')
    item_description = models.TextField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    size_chart = models.CharField(max_length=5, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50)
    available_from = models.DateField(help_text="Available start date")
    available_to = models.DateField(help_text="Available end date")

    def available_days(self):
        """Calculate total days available"""
        if self.available_from and self.available_to:
            return (self.available_to - self.available_from).days
        return 0

    def __str__(self):
        return self.item_name
# email
class Contact(models.Model):
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email   
# add to cart
class cart_Tbl(models.Model):
    u_name=models.ForeignKey(reg_Tbl,on_delete=models.CASCADE)
    product_name=models.ForeignKey(product_Tbl,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
# place order (CANCELL)
class Order_Tbl(models.Model):
    product = models.ForeignKey(product_Tbl, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")
    
    def __str__(self):
        return f"Order #{self.id} - {self.product.item_name}"
    
# payment
class Order(models.Model):
    user = models.ForeignKey(reg_Tbl, on_delete=models.CASCADE)
    product = models.ForeignKey(product_Tbl, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.name}"
    
