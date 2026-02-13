from django.contrib import admin
from .models import Category, Product, Wishlist, Cart, CartItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.site_header = "Veraux Admin"
admin.site.site_title = "Veraux Administration"
admin.site.index_title = "Welcome to Veraux Management"
