from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, JsonResponse
from shop.utils.choice import *
from shop.services.service import *
import uuid

# Create your views here.

CART_COOKIE_KEY = 'cart-token'
SHOPPING_CART = 'shopping_cart'


def index(request):
    context = getContext(request)
    alerts = []
    products = Product.objects.all()
    context['products'] = products
    context['rate'] = 24
    context = filterContext(context)
    response = render(request, 'shop/home/index.html', context)
    return myResponse(response, context)

@csrf_exempt
def addToCart(request: HttpRequest, token: uuid):
    context = getContext(request)
    alerts = []
    cart_token = request.COOKIES.get(CART_COOKIE_KEY)
    cart = None
    size = request.POST.get('size')
    if size:
        size = Size.objects.get(id=size)
    quantity = request.POST.get('quantity')

    if (quantity == None):
        return redirect('shop/home/index.html')

    tag = None
    if (token):
        tag = Tag.objects.filter(token=token).first()
    
    if tag == None:
        return redirect('shop/home/index.html')

    if cart_token:
        cart = Cart.objects.get(token=cart_token)
    
    if not cart:
        customer = None
        if request.user and request.user.is_authenticated:
            customer = request.user
        cart = Cart.createCartAndSave(customer)
    else:
        if context.get(SHOPPING_CART) and cart.checked_out:
            del context[SHOPPING_CART]

    if cart and not cart.checked_out:
        image = None
        tag_image_set = getProductImageSetInColorSet(tag.product, [tag.color])
        if tag_image_set and len(tag_image_set) > 0:
            image = tag_image_set[0]
        addItemAndSave(cart, tag, size, int(quantity), image)
        context[SHOPPING_CART] = cart


    context = filterContext(context)

    response = render(request, 'shop/includes/cart-items-container.html', context)
    response.set_cookie(key=CART_COOKIE_KEY, value=cart.token, max_age=155520000)

    return myResponse(response, context)

def product(request: HttpRequest, token: uuid):
    context = getContext(request)
    alerts = []
    if (token):
        product = Product.objects.filter(token=token).first()
        if product:
            context['selected_product'] = product

    context['products'] = products
    context = filterContext(context)
    response = render(request, 'shop/includes/product-detail-modal.html', context)
    return myResponse(response, context)

def products(request: HttpRequest):
    context = getContext(request)
    alerts = []
    products = Product.objects.filter(customer_viewable=True).all()
    product_token = request.GET.get('product_token')
    if (product_token):
        product = Product.objects.filter(token=product_token).first()
        if product:
            context['selected_product'] = product
    context['products'] = products
    context = filterContext(context)
    response = render(request, 'shop/home/products.html', context)
    return myResponse(response, context)

def brands(request):
    context = getContext(request)
    alerts = []
    brands = Brand.objects.filter(selectable=True)
    context['brands'] = brands
    context = filterContext(context)
    response = render(request, 'shop/home/brands.html', context)
    return myResponse(response, context)

def brand(request, slug):
    context = getContext(request)
    alerts = []
    parameters = {}
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.filter(brand=brand)
    context['products'] = products
    context = filterContext(context)
    response = render(request, 'shop/home/brand-products.html', context)
    return myResponse(response, context)

def clothes(request):
    return product_by_category(request, 'clothes')

def snacks(request):
    return product_by_category(request, 'snack')

def product_by_category(request, category_str):
    context = getContext(request)
    alerts = []
    category = get_object_or_404(Category, name=category_str)
    print(category.related_products.all())
    products = category.related_products.all()
    context['products'] = products
    context = filterContext(context)
    response = render(request, 'shop/home/products.html', context)
    return myResponse(response, context)

def cart_add_item(request : HttpRequest):
    context = getContext(request)
    alerts = []
    cart : Cart = None
    item_tag_token = request.POST.get('item_tag_token')
    item_quantity : int = request.POST.get('item_quantity')
    tag:Tag = Tag.objects.filter(token=item_tag_token)
    if not item_quantity or item_quantity == 0:
        alerts.append(Alert(AlertTypeChoices.ERROR, "數量有誤", ""))
        context['alerts'] = alerts

        context = filterContext(context)
        response = render(request, request.META.get('HTTP_REFERER'), context)
        return myResponse(response, context)

    user = request.user
    if (not user.is_authenticated):
        user = None
    if user:
        cart = user.related_customer.getMostRecentActiveCart()
    elif (request.COOKIES.get(CART_COOKIE_KEY)):
        cart = get_object_or_404(request.COOKIES.get(CART_COOKIE_KEY))
    if (not cart):
        cart = Cart.createCart(user)
    success = cart.addItemAndSave(tag, item_quantity)
    if success and item_quantity > 0:
        alerts.append(Alert(AlertTypeChoices.INFO, "添加成功", ""))
    elif success and item_quantity < 0:
        alerts.append(Alert(AlertTypeChoices.INFO, "刪減成功", ""))
    else:
        alerts.append(Alert(AlertTypeChoices.WARNING, "操作失敗", ""))
    context['alerts'] = alerts
    context = filterContext(context)
    response = render(request, request.META.get('HTTP_REFERER'), context)
    return myResponse(response, context)



def rate_converter(request):
    return render(request, 'shop/home/rate-converter.html', {})

def getContext(request: HttpRequest):
    context = {}
    if request and request.COOKIES.get(CART_COOKIE_KEY):
        cart = Cart.objects.get(token=request.COOKIES.get(CART_COOKIE_KEY))
        request.COOKIES.update()
        if cart:
            context[SHOPPING_CART] = cart
    return context

@csrf_exempt
def updateCart(request: HttpRequest):
    data = {}
    alerts = []
    cartToken = request.POST.get('cart_token')
    itemToken = request.POST.get('item_token')
    quantity = request.POST.get('quantity')
    quantity = int(quantity)
    if (not cartToken or not itemToken or not isinstance(quantity, int)):
        return JsonResponse(status=400,data={})

    cart: Cart = Cart.objects.get(token=cartToken)
    item: CartItem = None
    if cart:
        item = cart.item_set.get(token=itemToken)
    if item:
        item.updateQuantityAndSave(quantity)
        if item.quantity == 0:
            cart.item_set.remove(item)
            cart.save()
        data['quantity'] = item.quantity
    else:
        return JsonResponse(status=400, data=data)
    
    response = JsonResponse(data=data)
    return response

def checkoutView(request: HttpRequest):
    context = getContext(request)
    context['remove_cart_toggler'] = True
    response = render(request, 'shop/home/check-out.html', context)
    return myResponse(response, context)
        


def filterContext(context: dict):
    
    cart : Cart = context.get(SHOPPING_CART)
    if cart:
        if cart.checked_out:
            del context[SHOPPING_CART]
    return context

def myResponse(response: HttpResponse, context: dict):
    if response.cookies.get(CART_COOKIE_KEY) and not context.get(SHOPPING_CART):
        response.set_cookie(key=CART_COOKIE_KEY, value="", max_age=0)
    return response
        
