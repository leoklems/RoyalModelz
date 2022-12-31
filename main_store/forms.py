from django import forms
from django.forms import ModelForm, Textarea, TextInput, ClearableFileInput, MultipleChoiceField, \
    CheckboxSelectMultiple, Select, CheckboxInput, SelectMultiple
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        error_messages = {
            'password1': {
                'required': _("this field is required."),
                'invalid': _("chose a valid password"),
                'validator': _("chose a valid password"),
            },
            'password2': {
                'required': _("this field is required."),
                'invalid': _("chose a valid password"),
                'validator': _("passwords don't match"),
            },
            'username': {
                'required': _("country field required."),
                'invalid': _("username should be less than 10 characters"),
                'validator': _("username should be less than 10 characters"),
            },
            'email': {
                'required': _("email field is required."),
                'invalid': _("please put a valid email address"),
                'validator': _("please put a valid email address"),
            },
        }


class AuthorProfileForm(ModelForm):
    class Meta:
        model = Author
        field = '__all__'
        exclude = ['user', 'uid', 'date_registered']
        error_messages = {
            'profile_pic': {
                'invalid': _("put a valid image file"),
            },
            # 'phone_no': {
            #     'invalid': _("put in a valid phone number"),
            # },

        }
        widgets = {
            'title': Select(attrs={
                'class': 'form-control',
            }),
            'gender': SelectMultiple(attrs={
                'class': 'form-control',
            }),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        field = '__all__'
        exclude = ['author', 'product_id', 'date_added']

        widgets = {
            'categorys': SelectMultiple(attrs={
                'class': 'form__cat__item',
            }),

        }


class ProductCatForm(ModelForm):
    class Meta:
        model = ProductCategory
        field = '__all__'
        exclude = []


class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        field = '__all__'
        exclude = ['date_added']

        # widgets = {
        #     'leads': CheckboxInput(attrs={
        #         'class': 'form-check-input',
        #     }),
        # }


class SlideForm(ModelForm):
    class Meta:
        model = Slide
        field = '__all__'
        exclude = ['']


class FirstnameChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name']


class SurnameChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ['last_name']


class ProductNameChangeForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name']
        widgets = {
            'name': Select(attrs={
                'class': 'form-control',
            }),

        }


class ProductCategoryChangeForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category']
        # widgets = {
        #     'category': SelectMultiple(attrs={
        #         'class': 'form__cat__item',
        #         'value': '{{object.category}}',
        #     }),
        #
        # }


class ProductBrandChangeForm(ModelForm):
    class Meta:
        model = Product
        fields = ['brand']
        widgets = {
            'brand': Select(attrs={
                'class': 'form-control',
            }),

        }


class ProductColorsChangeForm(ModelForm):
    class Meta:
        model = Product
        fields = ['colors']
        widgets = {
            'colors': Select(attrs={
                'class': 'form-control',
            }),

        }


class ProductSizesChangeForm(ModelForm):
    class Meta:
        model = Product
        fields = ['sizes']
        widgets = {
            'name': Select(attrs={
                'class': 'form-control',
            }),

        }


class ProductPriceChangeForm(ModelForm):
    class Meta:
        model = Product
        fields = ['price']
        widgets = {
            'price': Select(attrs={
                'class': 'form-control',
            }),

        }


class ProductDiscountPriceChangeForm(ModelForm):
    class Meta:
        model = Product
        fields = ['discount_price']
        widgets = {
            'discount_price': Select(attrs={
                'class': 'form-control',
            }),

        }


class ProductProductImageChangeForm(ModelForm):
    class Meta:
        model = ProductImage
        field = '__all__'
        exclude = ['date_added']
        # widgets = {
        #     'product': SelectMultiple(attrs={
        #         'value': '{{object.product_images.name}}',
        #     }),
        #     'lead': SelectMultiple(attrs={
        #         'value': '{{object.lead}}',
        #     }),
        #
        # }

