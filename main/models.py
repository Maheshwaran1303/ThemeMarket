from django.db import models

class HomeTemplate(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='UX-themes')
    image = models.ImageField(upload_to='ui_templates/')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=99)
    rating = models.FloatField(default=4.0)
    sales = models.PositiveIntegerField(default=205)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class HomeProduct(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100, default='UX-themes')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=99)
    rating = models.FloatField(default=4)
    sales = models.PositiveIntegerField(default=205)
    image = models.ImageField(upload_to='products/')
    live_preview = models.URLField(blank=True, null=True)
    is_featured_themes = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('weekly', 'This Week'),
        ('monthly', 'This Month'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.CharField(max_length=100, blank=True)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100, default="UX-themes")
    rating = models.FloatField(default=4.5)
    sales = models.IntegerField(default=0)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='weekly')
    live_preview = models.URLField(blank=True)
    is_new = models.BooleanField(default=False)  # ✅ New field


    def __str__(self):
        return self.title


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# THEMES PAGE
class WordPressSection(models.Model):
    title = models.CharField(max_length=100, default="WordPress Themes")
    description = models.TextField(
        default="Discover premium WordPress themes crafted by top designers and developers. Each theme is carefully reviewed for quality, performance, and design excellence."
    )
    image = models.ImageField(upload_to='wordpress/', blank=True, null=True)

    def __str__(self):
        return self.title



class ThemeProduct(models.Model):
    CATEGORY_CHOICES = [
        ('Business', 'Business'),
        ('Portfolio', 'Portfolio'),
        ('Blog', 'Blog'),
        ('E-Commerce', 'E-Commerce'),
        ('Landing Page', 'Landing Page'),
    ]

    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100, default='UX-themes')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.FloatField(default=4)
    sales = models.PositiveIntegerField(default=205)
    image = models.ImageField(upload_to='themes/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='WordPress')
    features = models.TextField(blank=True)
    compatibility = models.CharField(max_length=100, blank=True)
    is_best_seller = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# TEMPLATES PAGE


from django.db import models

class TemplateItem(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='templates/')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


from django.db import models

class UITemplate(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='UX-themes')
    image = models.ImageField(upload_to='ui_templates/')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=99)
    rating = models.FloatField(default=4.0)
    sales = models.PositiveIntegerField(default=205)
    is_ui_template = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_top_seller = models.BooleanField(default=False)
    is_top_clean_item = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# About Page

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='team_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


# Contact Page


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


from django.contrib.auth.models import User

# Cart Page


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(UITemplate, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.template.price * self.quantity

    def __str__(self):
        return f"{self.template.name} x {self.quantity}"

# Chechout Page

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone_code = models.CharField(max_length=5, default="+91")
    phone_number = models.CharField(max_length=20)
    flat_no = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    landmark = models.CharField(max_length=255, blank=True)
    same_address = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout by {self.user.username} - {self.total}"


# Payment 

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    card_number = models.CharField(max_length=20, blank=True)
    expiry = models.CharField(max_length=10, null=True, blank=True)
    cvv = models.CharField(max_length=5, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return f"Payment - {self.user.username} - {self.payment_method}"
