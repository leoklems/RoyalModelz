from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.urls import reverse


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Author(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    TITLE = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Ms', 'Ms'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="author", blank=True)
    uid = models.SlugField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=7, choices=GENDER, null=True, blank=True)
    title = models.CharField(max_length=7, default='', choices=TITLE, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default="media/profile_pix.png", null=True, blank=True)
    reg_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Activity(models.Model):
    TYPE = (
        ('Login', 'Login'),
        ('Logout', 'Logout'),
        ('Add', 'Add'),
        ('Update', 'Update'),
        ('Delete', 'Delete'),
    )
    actor = models.ForeignKey(Author, on_delete=models.CASCADE,
                              related_name="actor", blank=True)
    type = models.CharField(max_length=7, default='', choices=TYPE, null=True, blank=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    action_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} {self.action_date} {self.type}"


class Slide(models.Model):
    index = models.IntegerField(null=True, blank=True)
    link = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='slides/', default="media/default_slider.jpg", blank=True, null=True)

    class Meta:
        ordering = ("index",)

    def __str__(self):
        return f"slide - {self.index}"


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=100)
    colors = models.CharField(max_length=100)
    sizes = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 blank=True, null=True, related_name="product_categories")
    author = models.ForeignKey(Author, related_name='product_author', on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.SlugField(max_length=20, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    discount_price = models.FloatField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0, null=True, blank=True)

    def percentage_discount(self):
        try:
            new_price = self.discount_price
            old_price = self.price
            perc_price = ((old_price - new_price)/old_price)*100
            return int(perc_price)
        except:
            return 0

    def __str__(self):
        return f"{self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                     blank=True, null=True, related_name="product_images")
    file = models.ImageField(upload_to='product/images/')
    lead = models.BooleanField(default=False, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"img - {self.product}"


class ProductOrder(models.Model):
    email = models.EmailField(max_length=50, blank=True, null=True,)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                 blank=True, null=True, related_name="product_order")
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    complete = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_follow_url(self):
        return reverse("store:order_product", kwargs={"pid": self.product.product_id})

    def __str__(self):
        return f"{self.product} - {self.pk}"
