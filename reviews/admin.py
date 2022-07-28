
from django.contrib import admin
from .models import Image, Product, Company, Comment, Category, ProductSize, ProductSite
from django.contrib.auth.models import Group

# # Register your models here.
# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Company)
# admin.site.register(ProductSize)
# admin.site.register(ProductSite)
# admin.site.register(Comment)

# #unregister the group model in the admin page
# admin.site.unregister(Group)

# # changing the Title of the admin page
# admin.site.site_header ="Makarios Product Review Admin Page"




# Another way of congiguring the admin page is the use of class and the admin decorator

@admin.register(Product)
class ProductAdmin_Page(admin.ModelAdmin):
    list_display = ("pk", "name", "content", )
    list_filter = ["category"]
    pass
    # admin.site.register(Product)
    admin.site.register(Category)
    admin.site.register(Company)
    admin.site.register(ProductSize)
    admin.site.register(ProductSite)
    admin.site.register(Comment)
    admin.site.register(Image)

    #unregister the group model in the admin page
    admin.site.unregister(Group)

    # changing the Title of the admin page
    admin.site.site_header ="Makarios Product Review Admin Page"