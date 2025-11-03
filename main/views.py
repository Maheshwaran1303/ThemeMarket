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


from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import ThemeProduct


def filter_themes(request):
    """AJAX Filtering with Grid/List View and No Results Handling"""
    sort_option = request.GET.get('sort', 'best')
    category = request.GET.get('category', '')
    price = request.GET.get('price', '')
    rating = request.GET.get('rating', '')
    features = request.GET.get('features', '')
    compatibility = request.GET.get('compatibility', '')
    view_mode = request.GET.get('view', 'grid')  # 'grid' or 'list'

    # Base queryset
    products = ThemeProduct.objects.all()

    # --- CATEGORY FILTER ---
    if category and category.lower() != 'all':
        products = products.filter(category__icontains=category)

    # --- PRICE FILTER ---
    if price == 'low':
        products = products.filter(price__lt=20)
    elif price == 'medium':
        products = products.filter(price__gte=20, price__lte=50)
    elif price == 'high':
        products = products.filter(price__gt=50)

    # --- RATING FILTER ---
    if rating == '4':
        products = products.filter(rating__gte=4)
    elif rating == '3':
        products = products.filter(rating__gte=3)

    # --- FEATURES FILTER ---
    if features and features.lower() != 'all':
        products = products.filter(features__icontains=features)

    # --- COMPATIBILITY FILTER ---
    if compatibility and compatibility.lower() != 'all':
        products = products.filter(compatibility__icontains=compatibility)

    # --- SORTING OPTIONS ---
    if sort_option == 'popular':
        products = products.filter(is_popular=True)
    elif sort_option == 'newest':
        products = products.order_by('-created_at')
    elif sort_option == 'low':
        products = products.order_by('price')
    elif sort_option == 'high':
        products = products.order_by('-price')
    else:  # best sellers
        products = products.filter(is_best_seller=True)

    # --- RENDER PRODUCT HTML (Grid or List) ---
    html = render_to_string('main/include/product_cards.html', {
        'products': products,
        'view_mode': view_mode,  # pass layout mode to template
    })

    # --- HANDLE NO PRODUCTS FOUND CASE ---
    if not products.exists():
        html = """
        <div class="no-products-found text-center py-5">
            <img src="/static/images/no-results.svg" alt="No Results" class="no-results-img mb-3">
            <h5>No matching products found</h5>
            <p class="text-muted">Try adjusting your filters or search criteria.</p>
        </div>
        """

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


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# 🟢 REGISTER
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
import re

# ✅ AJAX Email Availability Checker
def check_email_exists(request):
    email = request.GET.get('email', '').strip()
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})

# ✅ Register User View
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # --- Validation Checks ---
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if not re.match(r'^[A-Za-z\s]{3,}$', username):
            messages.error(request, 'Enter a valid name (letters only, min 3 chars).')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please login instead.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # --- Create User ---
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully! Please login.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('/')

# 🟠 LOGIN
def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Since Django auth uses username, find it by email
        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
        else:
            messages.error(request, 'Invalid credentials.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')

# 🔴 LOGOUT
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('/')



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


from django.http import JsonResponse # Ensure this is imported at the top

@login_required(login_url='main:login')
def add_to_cart(request, template_id):
    template = get_object_or_404(UITemplate, id=template_id)

    # Check if already in cart
    cart_item, created = CartItem.objects.get_or_create(user=request.user, template=template)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        message_type = "updated"
    else:
        message_type = "added"
    
    # Cart item count (for updating the header icon)
    cart_count = CartItem.objects.filter(user=request.user).count()

    # 🎯 CRITICAL FIX: Return JSON data instead of redirecting
    return JsonResponse({
        'success': True,
        'message_type': message_type,
        'cart_count': cart_count,
        'item': {
            'id': template.id,
            'name': template.name,
            'price': float(template.price), # Convert Decimal for JSON
            'image_url': template.image.url if template.image else '',
        }
    })




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

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Add some items first.")
        return redirect('main:cart')

    total = sum(item.subtotal() for item in cart_items)
    # The current discount calculation is 3% of total
    discount = total * Decimal('0.03') 
    grand_total = total - discount

    if request.method == "POST":
        # Collect Data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_code = request.POST.get('phone_code', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        flat_no = request.POST.get('flat_no', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        landmark = request.POST.get('landmark', '').strip()
        same_address = request.POST.get('same_address') == 'on'

        # ✅ Backend Validation
        errors = []
        if not first_name or not email or not phone_number or not flat_no or not address or not city or not state or not postal_code:
            errors.append("Please fill in all required fields.")

        # Email Validation
        try:
            validate_email(email)
        except ValidationError:
            errors.append("Enter a valid email address.")

        # Phone Validation
        if not re.match(r'^\d{6,15}$', phone_number):
            errors.append("Enter a valid phone number (6–15 digits).")

        # Postal Code Validation
        if not re.match(r'^\d{4,10}$', postal_code):
            errors.append("Enter a valid postal code.")

        if errors:
            for e in errors:
                messages.error(request, e)
            # Re-render the form with errors
            return render(request, 'main/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'discount': discount,
                'grand_total': grand_total,
            })

        # ✅ Save to DB if all validations pass
        # This saves the checkout data before moving to payment
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

        # 🎯 CRITICAL CHANGE: Redirect to payment page AFTER successful checkout submission
        messages.success(request, "Billing details saved! Choose your payment method.")
        return redirect('main:payment')

    return render(request, 'main/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'grand_total': grand_total,
    })


from .models import CartItem, Checkout, Payment
from decimal import Decimal
import uuid # 👈 Ensure this import is present
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404 # Ensure get_object_or_404 is imported

# ...

from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem, Checkout, Payment
import uuid 
# ... மற்ற imports ...

@login_required
def payment_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Nothing to pay for.")
        return redirect('main:cart')
    
    # Calculate Totals for display (required for both GET and POST)
    total = sum(item.subtotal() for item in cart_items)
    discount = total * Decimal('0.03') 
    grand_total = total - discount
    
    context = {
        'cart_items': cart_items,
        'total': total, 
        'discount': discount, 
        'grand_total': grand_total, 
    }

    if request.method == "POST":
        # 🟢 POST Request (Payment Submission Logic)
        try:
            latest_checkout = Checkout.objects.filter(user=request.user).latest('date')
            payment_amount = latest_checkout.total
        except Checkout.DoesNotExist:
            messages.error(request, "Checkout details not found. Please complete checkout again.")
            return redirect('main:checkout')
        
        payment_method = request.POST.get('payment_method')
        
        # Save Payment Record
        new_transaction_id = uuid.uuid4().hex[:12]
        payment_record = Payment.objects.create(
            user=request.user,
            payment_method=payment_method,
            total=payment_amount, 
            transaction_id=new_transaction_id 
        )
        
        # Clear cart and checkout record
        cart_items.delete() 
        latest_checkout.delete()

        # Redirect to success page
        return redirect('main:payment_success', payment_id=payment_record.id)


    # 🎯 CRITICAL FIX: Add the return statement for the GET Request!
    # 🔵 GET Request (Page Load Logic)
    return render(request, 'main/payment.html', context)



@login_required
def payment_success(request, payment_id): # ✅ payment_id argument added
    # 🎯 FIX: Get the payment record instead of relying on session/URL params
    payment_record = get_object_or_404(Payment, id=payment_id, user=request.user)

    # Save values to session for PDF download
    request.session['last_payment'] = {
        'transaction_id': payment_record.transaction_id,
        'total': float(payment_record.total), # Convert Decimal to float for session
        'method': payment_record.payment_method,
        'date': payment_record.date.strftime("%d %B %Y"),
    }

    return render(request, 'main/payment_success.html', {
        'transaction_id': payment_record.transaction_id,
        'total': payment_record.total,
        'payment_method': payment_record.payment_method,
        'date': payment_record.date.strftime("%d %B %Y"),
    })

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import datetime
from django.http import HttpResponse

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

