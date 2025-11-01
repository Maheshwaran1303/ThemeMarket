from django.shortcuts import render, redirect
from django.contrib import messages   

from .models import Product, Subscription

from .models import HomeProduct,TemplateItem, UITemplate

def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if Subscription.objects.filter(email=email).exists():
                messages.warning(request, "You're already subscribed!")
            else:
                Subscription.objects.create(email=email)
                messages.success(request, "Thank you for subscribing! Check your inbox soon.")
        return redirect('main:home')
    
    featured_themes = HomeProduct.objects.filter(is_featured_themes=True)[:6]  
    trending_products = Product.objects.filter(is_trending=True)[:3]
    week_products = Product.objects.filter(category='weekly')[:3]
    month_products = Product.objects.filter(category='monthly')[:3]
    new_arrivals = Product.objects.filter(is_new=True)[:6]
    featured_items = TemplateItem.objects.filter(is_featured=True)[:2]
    templates = UITemplate.objects.filter(is_ui_template=True)[:3]


    return render(request, 'main/home.html', {
        'featured_themes': featured_themes,
        'trending_products': trending_products,
        'week_products': week_products,
        'month_products': month_products,
        'new_arrivals': new_arrivals,
        'featured_items': featured_items,
        'templates': templates
    })


from .models import WordPressSection, ThemeProduct


from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import ThemeProduct


def themes(request):
    """Main Themes Page"""
    section = WordPressSection.objects.first() 
    products = ThemeProduct.objects.all()
    return render(request, 'main/themes.html', {
        'section': section,
        'products': products,
    })


def filter_themes(request):
    """AJAX Filtering"""
    sort_option = request.GET.get('sort', 'best')
    category = request.GET.get('category', '')
    price = request.GET.get('price', '')
    rating = request.GET.get('rating', '')
    features = request.GET.get('features', '')
    compatibility = request.GET.get('compatibility', '')
    view_mode = request.GET.get('view', 'grid')

    products = ThemeProduct.objects.all()

    # --- Category Filter ---
    if category and category != 'All':
        products = products.filter(category=category)

    # --- Price Filter ---
    if price == 'low':
        products = products.filter(price__lt=20)
    elif price == 'medium':
        products = products.filter(price__range=(20, 50))
    elif price == 'high':
        products = products.filter(price__gte=50)

    # --- Rating Filter ---
    if rating == '4':
        products = products.filter(rating__gte=4)
    elif rating == '3':
        products = products.filter(rating__gte=3)

    # --- Features Filter ---
    if features and features != 'All':
        products = products.filter(features__icontains=features)

    # --- Compatibility Filter ---
    if compatibility and compatibility != 'All':
        products = products.filter(compatibility__icontains=compatibility)

    # --- Sorting ---
    if sort_option == 'popular':
        products = products.filter(is_popular=True)
    elif sort_option == 'newest':
        products = products.order_by('-created_at')
    elif sort_option == 'low':
        products = products.order_by('price')
    elif sort_option == 'high':
        products = products.order_by('-price')
    else:
        products = products.filter(is_best_seller=True)

    html = render_to_string('main/include/product_cards.html', {
        'products': products,
        'view_mode': view_mode
    })
    return JsonResponse({'html': html})


from django.shortcuts import render
from .models import TemplateItem, UITemplate

# Tempaltes Page

def templates_page(request):
    featured_items = TemplateItem.objects.filter(is_featured=True)[:2]
    templates = UITemplate.objects.filter(is_ui_template=True)[:3]
    best_sellers = UITemplate.objects.filter(is_best_seller=True)[:6]
    top_sellers = UITemplate.objects.filter(is_top_seller=True)[:3]
    top_clean_items = UITemplate.objects.filter(is_top_clean_item=True)[:3]
    
    return render(request, 'main/templates.html', {
        'featured_items': featured_items,
        'templates': templates,
        'best_sellers': best_sellers,
        'top_sellers': top_sellers,
        'top_clean_items': top_clean_items
    })

from .models import TeamMember

def about(request):
    team_members = TeamMember.objects.all()
    return render(request, "main/about.html", {'team_members': team_members})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if first_name and email and message:
            ContactMessage.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                message=message
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('main:contact')
        else:
            messages.error(request, "Please fill out all required fields.")

    return render(request, 'main/contact.html')


# Register
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please fill in all fields.")
            return redirect('main:register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists. Try a different one.")
            return redirect('main:register')

        user = User.objects.create_user(username=username, password=password)
        user.save()

        # ✅ Automatically log the user in after registration
        login(request, user)
        messages.success(request, f"Welcome {user.username}! Your account has been created successfully.")
        return redirect('main:home')

    return render(request, 'main/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('main:home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('main:login')

    return render(request, 'main/login.html')


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('main:home')



def logout_user(request):
    logout(request)
    messages.info(request, "You have logged out successfully.")
    return redirect('main:home')


# Cart Page

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import UITemplate, CartItem

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)

    # Proper Decimal usage
    savings_rate = Decimal('0.045')
    savings = total * savings_rate
    grand_total = total - savings

    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'savings': savings,
        'grand_total': grand_total,
    })


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import UITemplate, CartItem

@login_required(login_url='main:login')  # 👈 Redirects anonymous users to login
def add_to_cart(request, template_id):
    template = get_object_or_404(UITemplate, id=template_id)

    # Check if already in cart
    cart_item, created = CartItem.objects.get_or_create(user=request.user, template=template)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, f"Quantity updated for '{template.name}'.")
    else:
        messages.success(request, f"✅ '{template.name}' added to your cart!")

    return redirect('main:cart')




@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.info(request, "Item removed from your cart.")
    return redirect('main:cart')


@login_required
def empty_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    messages.info(request, "Your cart has been emptied.")
    return redirect('main:templates')

from django.http import JsonResponse

@login_required
def update_cart_quantity(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        action = request.POST.get("action")

        try:
            item = CartItem.objects.get(id=item_id, user=request.user)
        except CartItem.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

        if action == "increase":
            item.quantity += 1
        elif action == "decrease" and item.quantity > 1:
            item.quantity -= 1
        item.save()

        total = sum(i.subtotal() for i in CartItem.objects.filter(user=request.user))
        savings_rate = Decimal('0.045')
        savings = total * savings_rate
        grand_total = total - savings

        return JsonResponse({
            "quantity": item.quantity,
            "subtotal": float(item.subtotal()),
            "total": float(total),
            "savings": float(savings),
            "grand_total": float(grand_total)
        })


from .models import Checkout

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Add some items first.")
        return redirect('main:cart')

    # Calculate totals
    total = sum(item.subtotal() for item in cart_items)
    discount = total * Decimal('0.03')  # 3% discount
    grand_total = total - discount

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_code = request.POST.get('phone_code')
        phone_number = request.POST.get('phone_number')
        flat_no = request.POST.get('flat_no')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        landmark = request.POST.get('landmark')
        same_address = request.POST.get('same_address') == 'on'

        Checkout.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_code=phone_code,
            phone_number=phone_number,
            flat_no=flat_no,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code,
            landmark=landmark,
            same_address=same_address,
            total=grand_total,
            discount=discount
        )

        messages.success(request, "✅ Checkout successful! Your order is being processed.")
        return redirect('main:payment')

    return render(request, 'main/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'grand_total': grand_total,
    })



from datetime import datetime
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import CartItem
from reportlab.pdfgen import canvas  # For PDF receipt generation


@login_required
def payment_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(float(item.subtotal()) for item in cart_items)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'Card')

        # Save details in session
        request.session['payment_total'] = float(total)
        request.session['payment_method'] = payment_method

        return redirect('main:payment_success')

    return render(request, 'main/payment.html', {'cart_items': cart_items, 'total': total})


@login_required
def payment_success(request):
    total = request.session.get('payment_total', 0)
    payment_method = request.session.get('payment_method', 'Card')
    transaction_id = random.randint(100000000000, 999999999999)
    date = datetime.now().strftime("%d %B %Y")

    # Clear cart after success
    CartItem.objects.filter(user=request.user).delete()

    # Save values to session for PDF download
    request.session['last_payment'] = {
        'transaction_id': transaction_id,
        'total': total,
        'method': payment_method,
        'date': date,
    }

    return render(request, 'main/payment_success.html', {
        'transaction_id': transaction_id,
        'total': total,
        'payment_method': payment_method,
        'date': date,
    })


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import datetime

@login_required
def download_receipt(request):
    payment = request.session.get('last_payment', None)
    if not payment:
        return HttpResponse("No recent payment found.")

    # PDF setup
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Receipt_{payment["transaction_id"]}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # --- Thememarket Header ---
    header_height = 60
    p.setFillColorRGB(0.26, 0.13, 0.51)  # Thememarket purple
    p.rect(0, height - header_height, width, header_height, fill=1)

    p.setFont("Helvetica-BoldOblique", 20)
    p.setFillColor(colors.white)
    p.drawString(40, height - 40, "Thememarket")

    # --- Title Section ---
    p.setFont("Helvetica-Bold", 18)
    p.setFillColor(colors.black)
    p.drawString(200, height - 100, "Payment Receipt")

    # --- Separator Line ---
    p.setStrokeColorRGB(0.26, 0.13, 0.51)
    p.setLineWidth(1)
    p.line(40, height - 110, width - 40, height - 110)

    # --- Payment Details Box ---
    p.setFont("Helvetica", 12)
    y = height - 160
    line_gap = 25

    p.setFillColor(colors.black)
    p.drawString(50, y, f"Transaction ID:")
    p.drawString(200, y, f"{payment['transaction_id']}")

    y -= line_gap
    p.drawString(50, y, "Date:")
    p.drawString(200, y, f"{payment['date']}")

    y -= line_gap
    p.drawString(50, y, "Payment Method:")
    p.drawString(200, y, f"{payment['method']}")

    y -= line_gap
    p.drawString(50, y, "Amount Paid:")
    p.drawString(200, y, f"US$ {payment['total']:.2f}")

    y -= line_gap
    p.drawString(50, y, "Status:")
    p.setFillColor(colors.green)
    p.drawString(200, y, "Success")

    # --- Footer ---
    p.setFillColor(colors.grey)
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 60, "Thank you for your purchase from Thememarket.")
    p.drawString(50, 45, "For support, contact: support@thememarket.com")

    p.showPage()
    p.save()
    return response



def login_view(request):
    return render(request, "main/login.html")

def register(request):
    return render(request, "main/register.html")

