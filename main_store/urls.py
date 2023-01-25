from django.urls import path

from .views import *
app_name = 'store'

urlpatterns = [

    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),

    path('', Home.as_view(), name='home'),
    path('product-detail/<product_id>/', ProductDetailView.as_view(), name='product'),

    path('admin-home/', AdminHome.as_view(), name='s_home'),
    path('staff/', AdminStaff.as_view(), name='s_staff'),
    path('staff-detail/<uid>/', StaffDetailView.as_view(), name='staff_detail'),
    path('staff-activities/<uid>/', StaffActivities.as_view(), name='staff_activities'),
    path('delete-staff/<uid>/', DeleteStaff.as_view(), name='delete_staff'),

    path('a-product-detail/<product_id>/', AdminProductDetailView.as_view(), name='staff_product_detail'),
    path('add-user/', AuthorRegistration.as_view(), name='add_staff'),
    path('admin-product-images/', AdminProductImages.as_view(), name='product_images'),

    path('add-product', AddProduct.as_view(), name='add_product'),
    path('delete-product/<product_id>/', DeleteProduct.as_view(), name='delete_product'),

    path('add-product-image', AddProductImage.as_view(), name='add_product_img'),
    path('delete-product-image/<pk>/', DeleteProductImage.as_view(), name='delete_product_img'),

    path('add-product-image', AddProductImage.as_view(), name='add_product_img'),
    path('update-product-image/<pk>/', UpdateProductImage.as_view(), name='update_product_img'),
    path('delete-product-image/<pk>/', DeleteProductImage.as_view(), name='delete_product_img'),

    path('add-product-category', AddProductCat.as_view(), name='add_product_cat'),
    path('update-product-category/<pk>/', UpdateProductCat.as_view(), name='update_product_cats'),
    path('delete-product-cat/<pk>/', DeleteProductCat.as_view(), name='delete_product_cat'),

    path('add-slide/', AddSlide.as_view(), name='add_slide'),
    path('update-slide/<pk>/', UpdateSlide.as_view(), name='update_slide'),
    path('delete-slide/<pk>/', DeleteSlide.as_view(), name='delete_slide'),

    path('update-first-name/<pk>/', FirstnameUpdate.as_view(), name='update_first_name'),
    path('update-surname/<pk>/', SurnameUpdate.as_view(), name='update_surname'),
    path('update-product-name/<product_id>/', ProductNameUpdate.as_view(), name='update_product_name'),
    path('update-product-product-category/<product_id>/', ProductCategoryUpdate.as_view(), name='update_product_cat'),
    path('update-product-brand/<product_id>/', ProductBrandUpdate.as_view(), name='update_product_brand'),
    path('update-product-color/<product_id>/', ProductColorsUpdate.as_view(), name='update_product_colors'),
    path('update-product-sizes/<product_id>/', ProductSizesUpdate.as_view(), name='update_product_sizes'),
    path('update-product-price/<product_id>/', ProductPriceUpdate.as_view(), name='update_product_price'),
    path('update-product-discount-price/<product_id>/', ProductDiscountPriceUpdate.as_view(),
         name='update_product_discount_price'),
    path('update-product-price-description/<product_id>/',
         ProductDescriptionUpdate.as_view(), name='update_product_description'),
    path('update-product-image-change/<pk>/', ProductProductImageUpdate.as_view(),
         name='update_product_image'),
    path('<pid>/order-product/', order_product, name='order_product'),
    path('update-product-order-status/<pk>/', ProductOrderStatusUpdate.as_view(), name='update_product_order_status'),
    path('orders/', AdminOrders.as_view(), name='admin_orders'),
]
