from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from .models import Contact, Order,cart_Tbl, product_Tbl, reg_Tbl
from django.conf import settings
from gc import get_objects
from django.contrib import messages
from django.core.mail import send_mail

# home
def home(request): 
    if request.method == "POST":
        email = request.POST.get("email")
        if email:  
            Contact.objects.create(email=email)
        return redirect('home')

    return render(request, "home.html")

# register
def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        mobile=request.POST.get('mobile')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_type=request.POST.get('user_type')
        confirm_password=request.POST.get('confirm_password')
        
        obj=reg_Tbl.objects.create(name=name,mobile=mobile,email=email,password=password,confirm_password=confirm_password,user_type=user_type)
        obj.save()
        msg='registered successfully'
        return render(request,'register.html',{'msg':msg})
    
    return render(request,'register.html')

# login

def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        obj=reg_Tbl.objects.filter(email=email,password=password)
        if obj.exists():
            for i in obj:
                id=i.id
                user_name=i.name
                user_mobile=i.mobile
                user_email=i.email
                user=i.user_type
            request.session['id']=id
            request.session['name']=user_name
            request.session['mobile']=user_mobile
            request.session['email']=user_email
            request.session['user_type']=user
            request.session['password']=password
            if user=='admin':
                return render(request,'admin.html')
            else:
                return render(request,'user.html')
    return render(request,'login.html')

# product view

def product(request):
    obj=product_Tbl.objects.all()
    return render(request,'product.html',{'obj':obj})

# add to cart

def cart(request):
    prod_id = request.GET.get('cid')
    user_id = request.session['id']

    prod_obj = get_object_or_404(product_Tbl, id=prod_id)
    user_obj = get_object_or_404(reg_Tbl, id=user_id)

    cart_item, created = cart_Tbl.objects.get_or_create(
        u_name=user_obj,
        product_name=prod_obj
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("view_cart")  


# single view of product

def product_detail(request, pk):
    product = get_object_or_404(product_Tbl, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

# remove from cart

def remove(request):
    id_no = request.GET.get('cid')
    obj = cart_Tbl.objects.filter(id=id_no)
    obj.delete()
    return redirect('view_cart')

# view cart 

def view_cart(request):
    user_id = request.session['id']
    user_obj = get_object_or_404(reg_Tbl, id=user_id)

    cart_items = cart_Tbl.objects.filter(u_name=user_obj)
    return render(request, 'view_cart.html', {'cart_items': cart_items})
# pay
def payment(request):
    user_id = request.session.get("id")
    user_obj = get_object_or_404(reg_Tbl, id=user_id)

    cart_items = cart_Tbl.objects.filter(u_name=user_obj)

    lines = []
    grand_total = 0

    for item in cart_items:
        product = item.product_name
        line_total = product.item_price * item.quantity
        grand_total += line_total
        lines.append({
            "product": product,
            "qty": item.quantity,
            "unit_price": product.item_price,
            "line_total": line_total,
        })
    cart_items.delete()

    return render(request, "payment.html", {
        "lines": lines,
        "grand_total": grand_total
    })
# success pop up 
def success(request):
    return render(request,'success.html')



####### ADMIN UI #######

def admin_additem(request):
    return render(request,'admin_additem.html')


def item_view(request):
        object=product_Tbl.objects.all()
        return render(request,'item_view.html',{'obj':object})

def admin_items(request):
    products = product_Tbl.objects.all()
    return render(request, 'admin_items.html', {'obj': products})


def admin_additem(request):
    quantity = request.POST.get('quantity') or 1 
    if request.method == 'POST':
        product_Tbl.objects.create(
            item_name=request.POST.get('item_name'),
            item_image=request.FILES.get('item_image'),
            item_description=request.POST.get('item_description'),
            item_price=request.POST.get('item_price'),
            gender=request.POST.get('gender'),
            quantity=quantity,
            size_chart=request.POST.get('size_chart'),
            color=request.POST.get('color'),
            available_from=request.POST.get('available_from'),
            available_to=request.POST.get('available_to'),
        )
        return redirect('item_view')

    return render(request, 'admin_additem.html')

def remove_item(request):
    pid = request.GET.get('cid')
    product = get_object_or_404(product_Tbl, id=pid)
    product.delete()
    return redirect('item_view')

def email(request):
    if request.method == "POST":

        user_email = request.POST.get('email')
        user_message = request.POST.get('message')

        Contact.objects.create(email=user_email, message=user_message)
        return redirect('home')

    obj = Contact.objects.all().order_by('-created_at')
    return render(request, 'email.html', {'obj': obj})

def user_list(request):
    users = reg_Tbl.objects.all()
    return render(request, 'user_list.html', {'users': users})
