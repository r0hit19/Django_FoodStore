import razorpay
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View


from . middlewaress.auth import auth_middleware
from django.utils.decorators import method_decorator

from . models import homepage,products,Category,Customers,Order
# Create your views here.
def home(request):

    obj3=homepage.objects.get(id=3)
    obj4 = homepage.objects.get(id=4)
    obj5 = homepage.objects.get(id=5)
    obj6 = homepage.objects.get(id=6)
    obj7 = homepage.objects.get(id=7)

    params={'objs3':obj3,'objs4':obj4,'objs5':obj5,'objs6':obj6,'objs7':obj7}
    return render(request,'homepage.html',params)

def menu(request):
    if request.method=='POST':
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1
        request.session['cart']=cart
        print(request.session['cart'])
        return redirect('menuitem')
    else:
        #request.session.clear()
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}
        prods = None
        categories = Category.get_all_categories()
        categoryid = (request.GET.get('category'))
        print(categoryid)
        if categoryid:
            prods = products.get_all_products_by_categoryid(categoryid)
        else:
            prods = products.get_all_product()
        data = {}
        data['products'] = prods
        data['categories'] = categories

        return render(request, 'menuitem.html', data)







def signup(request):
    if request.method=='GET':
        return render(request,'signup.html')
    else:
        first_name=request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        customer=Customers(first_name=first_name,
                           last_name=last_name,
                           email=email,
                           phone=phone,
                           password=password)
        customer.register()
        return redirect('login')

def login(request):
    return_url=None
    if request.method=='GET':
        login.return_url=request.GET.get('return_url')
        return render(request,'login.html')
    else:
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        customer=Customers.get_customer_by_phone(phone)
        error_message=''
        if customer:
            if password==customer.password:
                request.session['customer_id']=customer.id
                request.session['email'] =customer.email
                print(request.session['email'])
                if login.return_url:
                    return HttpResponseRedirect(login.return_url)
                else:
                    login.return_url=None
                    return redirect('menuitem')
            else:
                error_message='Phone or Password is invalid'
        else:
            error_message="Phone or Password is invalid"
            return render(request,'login.html',{'error':error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

class cart(View):

    def get(self,request):
        ids = (list(request.session.get('cart').keys()))
        product=(products.get_products_by_id(ids))
        return render(request,'cart.html',{'product':product})


def checkout(request):
    
    if request.method=='POST':
        address=request.POST.get('address')
        phone= request.POST.get('phone')
        mode=request.POST.get('mode')
        customers=request.session.get('customer_id')
        cart=request.session.get('cart')
        pro=products.get_products_by_id(cart.keys())
        print(address,phone,customers,cart,pro)

        for p in pro:
            order=Order(customer=Customers(id=customers),
                        product=p,
                        price=p.desc,
                        address=address,
                        phone=phone,
                        quantity=cart.get(str(p.id)),
                        mode=mode)

            order.save()

        if mode == "cash":
            request.session['cart'] = {}
            return redirect('confirmation')


        else:
            return redirect('payment')


        #return redirect('cart')

class orders(View):
    @method_decorator(auth_middleware)
    def get(self,request):
        customer=request.session.get('customer_id')
        order=Order.get_orders_by_customer(customer)

        return render(request,'orders.html',{'orders':order})

def payment(request):

    cart=(request.session.get('cart'))
    pro=products.get_products_by_id(cart.keys())

    sum=0
    product=""
    for p in pro:
        product+="-"+p.name
        sum=sum+int(p.desc)*int(cart.get(str(p.id)))
    price=sum*100
    c_id=(request.session.get('customer_id'))

    p_order=product
    request.session['cart']={}
    print(price)

    order_currency = 'INR'
    client=razorpay.Client(auth=('rzp_test_cpwtGRXKsWsMZl','Mee1zcQzXSp6bHqQWEPU4rIS'))
    #pay=client.order.create({"amount":price,"currency":'INR',"payment_capture":'1'})

    return render(request,'payment.html',{'price':price,'product':p_order,'c_id':c_id})


def confirmation(request):

    return render(request,'confirmation.html')


def aboutus(request):
    obj5 = homepage.objects.get(id=5)
    return render(request,'aboutus.html',{'obj5':obj5})