from contextlib import redirect_stderr
from django.shortcuts import HttpResponse, redirect
from django.http import JsonResponse 
from vendor.models import Vendor
from menu.models import Category,FoodItem
from vendor.models import Vendor, OpeningHour
from .models import Cart
from .context_processors import get_cart_counter,get_cart_amount

from django.shortcuts import get_object_or_404,render
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from datetime import date, datetime 

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    #print(vendors)
    context = {
        'vendors' : vendors,
        'vendor_count' : vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    category = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            # releted name in models.py
            'fooditem',
            queryset = FoodItem.objects.filter(is_available = True)
        )
    )

    # # add this item at last video no. 150
    # opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')
    # # print(opening_hours)
    # # # check opening hour is today
    # today_date = date.today().isoweekday()
    # # print(today_date)
    
    # current_opening_hour = OpeningHour.objects.filter(vendor=vendor, day = today_date)
    # # print(current_opening_hour)

    # current_time = datetime.now().strftime("%H:%M:%S")
    # # print(current_time)

    # is_open = None
    # for i in current_opening_hour:
    #     start = str(datetime.strptime(i.from_hour, "%I:%M %p").time())
    #     end = str(datetime.strptime(i.to_hour, "%I:%M %p").time())
    #     #print(start, end)
    #     if current_time > start and current_time < end:
    #         is_open = True
    #         break
    #     else:
    #         is_open = False
    # print(is_open)
    # # after addind member function in model
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')
    today_date = date.today().isoweekday()
    current_opening_hour = OpeningHour.objects.filter(vendor=vendor, day = today_date)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'cart_items' : cart_items,
        'vendor' : vendor,
        'category' : category,
        'opening_hours' : opening_hours,
        'current_opening_hour' : current_opening_hour,
        # 'is_open' : is_open,
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        #  return JsonResponse({'status': 'success' , 'message': 'User is logged in.'})
        if request. headers. get( 'x-requested-with') == 'XMLHttpRequest' :
            try:
                #food item exist or not in fooditem table
                fooditem = FoodItem.objects.get(id=food_id)
                #print(fooditem)
                # check if user is already added that food to the cart
                try:
                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # print(chkcart)
                    # increase the cart quantity
                    chkcart.quantity += 1
                    chkcart.save()
                    # print(chkcart.quantity)
                    return JsonResponse({'status': 'success' , 'message': 'Increase the cart quantity', 'cart_counter' : get_cart_counter(request), 'qty' : chkcart.quantity,'cart_amount' : get_cart_amount(request)})
                except:
                    # print("hiii")
                    chkcart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    # print("hiii")
                    return JsonResponse({'status': 'success' , 'message': 'Your new cart created', 'cart_counter' : get_cart_counter(request), 'qty' : chkcart.quantity,'cart_amount' : get_cart_amount(request)})
                    # print(chkcart.quantity)

            except:
                return JsonResponse({'status': 'Failed' , 'message': 'This food does no exist.'})
        else:
            return JsonResponse({'status': 'Failed' , 'message': 'Invalid request .'})
    else:
        return JsonResponse({'status': 'Login required !' , 'message': 'Please login to continue.'})

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        #  return JsonResponse({'status': 'success' , 'message': 'User is logged in.'})
        if request. headers. get( 'x-requested-with') == 'XMLHttpRequest' :
            try:
                #food item exist or not in fooditem table
                fooditem = FoodItem.objects.get(id=food_id)
                #print(fooditem)
                # check if user is already added that food to the cart
                try:
                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # print(chkcart)
                    if chkcart.quantity > 1:
                        # decrease the cart quantity
                        chkcart.quantity -= 1
                        chkcart.save()
                        # print(chkcart.quantity)
                    else:
                        chkcart.delete()
                        chkcart.quantity = 0
                    return JsonResponse({'status': 'success' , 'cart_counter' : get_cart_counter(request), 'qty' : chkcart.quantity ,'cart_amount' : get_cart_amount(request) })
                except:
                    # print("hiii")
                    return JsonResponse({'status': 'Failed' , 'message': 'do not have any of the items' })
                    # print(chkcart.quantity)

            except:
                return JsonResponse({'status': 'Failed' , 'message': 'This food does no exist.'})
        else:
            return JsonResponse({'status': 'Failed' , 'message': 'Invalid request .'})
    else:
        return JsonResponse({'status': 'Login required !' , 'message': 'Please login to continue.'})
    # return HttpResponse(food_id)


def delete_cart(request, cart_id):
     if request.user.is_authenticated:
        #  return JsonResponse({'status': 'success' , 'message': 'User is logged in.'})
        if request. headers. get( 'x-requested-with') == 'XMLHttpRequest' :
            try:
                #cart item in exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'success' , 'message': 'Your item deleted successfully', 'cart_counter' : get_cart_counter(request),'cart_amount' : get_cart_amount(request) })
            except:
                return JsonResponse({'status': 'Failed' , 'message': 'Cart item dose not exists.'})
        else:
            return JsonResponse({'status': 'Failed' , 'message': 'Invalid request .'})

@login_required(login_url='login')
def cart(request):
    cart_item = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_item' : cart_item,
    }
    return render(request, 'marketplace/cart.html', context)

def search(request):
    if not 'address' in request.path:
        return redirect('marketplace')
    else:
        # return HttpResponse("test")
        keyword = request.GET.get('keyword')
        address = request.GET.get('address')
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        radius = request.GET.get('radius')
        #print(keyword, address, lat, lng, radius)

        #get vendor ids that has the food item the user is user is looking for 
        fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
        # print(fetch_vendors_by_fooditems)

        vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
        #location base search
        if lat and lng and radius:
            pnt = GEOSGeometry('POINT(%s, %s)' % (lng, lat))

            vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, 
            user__is_active=True), user_profile__location__distance_lte=(pnt, D(km=radius))).annotate(distance=Distance("user_profile__location",pnt)).order_by("distance")

            for v in vendors:
                v.kms = round(v.distance.km, 1)
        # print(vendors)
        
        vendor_count = vendors.count()
        context = {
            'vendors' : vendors,
            'vendor_count' : vendor_count
        }

        return render(request, 'marketplace/listings.html' , context)