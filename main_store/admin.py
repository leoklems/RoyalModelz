from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Author)
admin.site.register(Activity)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Slide)
