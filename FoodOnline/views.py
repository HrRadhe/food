from django.shortcuts import render,redirect
from django.http import HttpResponse

from vendor.models import Vendor

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance



def home(request):
#     if 'lat' in request.GET:
#         pass
#         lat = request.GET['lat']
#         lng = request.GET['lng']
#         pnt = GEOSGeometry('POINT(%s, %s)' % (lng, lat))

#         vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=100))).annotate(distance=Distance("user_profile__location",pnt)).order_by("distance")

#         for v in vendors:
#                 v.kms = round(v.distance.km, 1)
#         return redirect('markterpalce')
        
#     else:
#         vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    #print(vendors)
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    context = {
        'vendors' : vendors,
    }
    return render(request,"home.html", context)