from django.contrib import admin
from .models import Product, HomeProduct

@admin.register(HomeProduct)
class HomeProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'is_featured_themes')
    list_filter = ('is_featured_themes',)
    search_fields = ('title', 'author')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_trending')
    list_filter = ('is_trending',)



from .models import WordPressSection

@admin.register(WordPressSection)
class WordPressThemeSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="120" style="border-radius:8px;">'
        return "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'


from .models import ThemeProduct

@admin.register(ThemeProduct)
class ThemeProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating', 'sales', 'image_preview')
    list_filter = ('category', 'is_best_seller', 'is_popular')
    search_fields = ('name', 'author')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="border-radius:6px;">'
        return 'No Image'
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'
    

from django.contrib import admin
from .models import TemplateItem

@admin.register(TemplateItem)
class TemplateItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_featured')
    list_filter = ('is_featured',)


from .models import UITemplate

@admin.register(UITemplate)
class UITemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'author', 'is_ui_template', 'is_best_seller', 'is_top_seller', 'is_top_clean_item')
    list_filter = ('is_ui_template', 'is_best_seller', 'is_top_seller', 'is_top_clean_item')


from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_at')
    search_fields = ('name', 'role')


from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at')
    search_fields = ('first_name', 'email')
    list_filter = ('created_at',)
