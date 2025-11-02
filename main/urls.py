from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("themes/", views.themes, name="themes"),
    path('themes/filter/', views.filter_themes, name='filter_themes'),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("templates/", views.templates_page, name="templates"),
    path("cart/", views.cart_view, name="cart"),
    path('cart/add/<int:template_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/empty/', views.empty_cart, name='empty_cart'),
    path('cart/update/', views.update_cart_quantity, name='update_cart_quantity'),
    path("checkout/", views.checkout_view, name="checkout"),
    path("payment/", views.payment_view, name="payment"),
    # path("payment-success/", views.payment_success, name="payment_success"),
    path('payment/success/<int:payment_id>/', views.payment_success, name='payment_success'), 
    path('payment/receipt/', views.download_receipt, name='download_receipt'),
    # path('invoice/download/', views.download_invoice, name='download_invoice'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('check-email/', views.check_email_exists, name='check_email_exists'),
]
