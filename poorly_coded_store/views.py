from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    quantity_from_form = int(request.POST["quantity"])
    #price_from_form = float(request.POST["price"])
    id_from_form = request.POST["product_id"]
    
    # getting price from product table
    this_product= Product.objects.get(id=id_from_form)
    
    price = this_product.price
    
    total_charge = quantity_from_form * price
    
    print("Charging credit card...")
    
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
    
    # calculating # of items ordered so far (returns dictionary)
    total_items = Order.objects.all().aggregate(Sum('quantity_ordered'))
    total_items = total_items['quantity_ordered__sum']
    
    # calculating total charged so far
    total_charged = Order.objects.all().aggregate(Sum('total_price'))
    total_charged = total_charged['total_price__sum']   
    
    # formatting total_charged
    total_charged= '{0:.2f}'.format(total_charged) 
    
    context = {
        'total_charge': total_charge,
        'total_items': total_items,
        'total_charged': total_charged
    }
    
    #return render(request, "store/checkout.html", context)
    return redirect("/")