from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amount
from .forms import OrderForm
from .models import Order, Payment, OrderedFood
import simplejson as json
from .utils import generate_oder_number
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def place_order(request):
    cart_item = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_item.count()
    if cart_count <= 0:
        return redirect('marketplace')

    subtotal = get_cart_amount(request)['subtotal']
    total_tax = get_cart_amount(request)['tax']
    grand_total = get_cart_amount(request)['grand_total']
    tax_data = get_cart_amount(request)['tax_dict']

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            #take from user
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            #other database fields
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment-method']
            #order.order_number = '123'
            order.save() # order id/pk generated
            order.order_number = generate_oder_number(order.id)
            order.save() # with order number
            context ={
                'order' : order,
                'cart_items' : cart_item,
            }
            return render(request, 'orders/place_order.html', context) # we want to sent order and cart item detail so we can't use "return redirect("#")"
        else:
            print(form.errors)

    # print(subtotal, total_tax, grand_total,tax_data)
    return render(request, 'orders/place_order.html')

@login_required(login_url='login')
def payments(request):
    # check if the request is ajax or not
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # STORE THE PAYMENT DETAILS IN THE PAYMENT MODEL
        order_number= request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        # print(order_number, transaction_id, payment_method, status)
        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            status = status,
            amount = order.total
        )
        payment.save()

        # UPDATE THE ORDER MODEL
        order.payment = payment
        order.is_ordered = True
        order.save()
        # return HttpResponse("done")

        # MOVE THE CART ITEMS TO ORDERED FOOD MODEL
        cart_items = Cart.objects.filter(user=request.user)
        # print(cart_items)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity 
            ordered_food.save()

        # return HttpResponse('saved ordered food')

        # SEND ORDER CONFIRMATION
        mail_subject = 'Thank you for ordering with us.'
        mail_template = 'orders/order_confirmation_email.html'
        context = {
            'user' : request.user,
            'order' : order,
            'to_email' : order.email,
        }
        send_notification(mail_subject, mail_template , context)
        # return HttpResponse('saved order confirmation and email is send')

        # SEND ORDER RECEIVED EMAIL TO THE VENDER
        mail_subject = 'You have received a new order.'
        mail_template = 'orders/new_order_received.html'
        to_emails = []
        for i in cart_items:
            if i.fooditem.vendor.user.email not in to_emails:
                to_emails.append(i.fooditem.vendor.user.email)
        # print(to_emails)
        context = {
            'order' : order,
            'to_email' : to_emails,
        }
        send_notification(mail_subject, mail_template , context)

        # CLEAR THE CART IF THE PAYMENT IS SUCCESS
        # cart_items.delete()

        # RETURN BACK TO AJAX WITH THE STATUS SUCCESS OR FAILURE
        response = {
            'order_number' : order_number,
            'transaction_id' : transaction_id,
        }
        return JsonResponse(response)

    return HttpResponse('payment view')

def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('transaction_id')
    print(order_number, transaction_id)

    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered = True)
        ordered_food = OrderedFood.objects.filter(order=order)

        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)
        
        tax_data = json.loads(order.tax_data)
        # print(tax_data)

        context = {
            'order' : order,
            'ordered_food' : ordered_food,
            'subtotal' : subtotal,
            'tax_data' : tax_data
        }
        return render(request, 'orders/order_complete.html' , context)

    except:
        return redirect('home')
    