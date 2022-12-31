from random import randint
from time import timezone

from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from itertools import chain
from django.core.mail import send_mail

from .forms import *
from .models import *
from django.db.models import Count
from django.db.models import Q

# Create your views here.


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,
                            password=password)
        print(user)

        if user is not None:
            login(request, user)
            staff = Author.objects.get(user=request.user)
            act = Activity(actor=staff, action='Login')
            act.save()
            return redirect('store:s_home')

        else:
            messages.info(request, 'username or password is incorrect')

    return render(request, 'forms/login.html')


def logoutUser(request):
    staff = Author.objects.get(user=request.user)
    act = Activity(actor=staff, action='Logout')
    act.save()
    logout(request)
    return redirect('store:login')


class Home(View):

    def get(self, *args, **kwargs):
        products = Product.objects.all()
        slides = Slide.objects.all()
        product_cats = ProductCategory.objects.all()
        product_images = ProductImage.objects.filter(lead=True)

        context = {
            'products': products,
            'slides': slides,
            'product_cats': product_cats,
            'product_images': product_images,
        }
        print([x.product for x in product_images])

        return render(self.request, 'home.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'
    slug_field = 'product_id'
    slug_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all().exclude(product_id=self.object.product_id)
        product_images = ProductImage.objects.filter(product=self.object)
        product_images_o = ProductImage.objects.filter(lead=True).exclude(product=self.object)
        product_cats = ProductCategory.objects.all()

        context["products"] = products
        context["product_images"] = product_images
        context["product_images_o"] = product_images_o
        context["product_cats"] = product_cats

        return context


# --------------------------------------Admin section-----------------------


class AdminHome(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        products = Product.objects.all()
        product_cats = ProductCategory.objects.all()
        slides = Slide.objects.all()
        staff = Author.objects.all()
        product_images = ProductImage.objects.filter(lead=True)

        context = {
            'products': products,
            'product_cats': product_cats,
            'slides': slides,
            'staff': staff,
            'product_images': product_images,
        }

        return render(self.request, 'staff/home.html', context)


class AdminStaff(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        staff = Author.objects.all()

        context = {
            'staff': staff,
        }

        return render(self.request, 'staff/staff.html', context)


class StaffDetailView(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'staff/staff-profile.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actor = Author.objects.get(user=self.object.user)
        acts = Activity.objects.filter(actor=self.object).order_by('-action_date')[:10]
        context["acts"] = acts
        return context


class StaffActivities(LoginRequiredMixin, DetailView):
    model = Author
    template_name = 'staff/staff-activities.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    # paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        acts = Activity.objects.filter(actor=self.object).order_by('-action_date')
        paginator = Paginator(acts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context["acts"] = page_obj
        return context


class AdminProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'staff/product_detail.html'
    slug_field = 'product_id'
    slug_url_kwarg = 'product_id'



class AdminProductImages(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        products = Product.objects.all()
        product_cats = ProductCategory.objects.all()
        product_images = ProductImage.objects.all()

        context = {
            'products': products,
            'product_cats': product_cats,
            'product_images': product_images,
        }
        print([x.product for x in product_images])

        return render(self.request, 'staff/product_images.html', context)


def random_int():
    random_ref = randint(0, 9999999999)
    uid = random_ref
    return uid


class AuthorRegistration(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('users.add_user', 'users.add_student')

    def get(self, request):
        form = CreateUserForm()
        profile_form = AuthorProfileForm()

        context = {
            'form': form,
            'profile_form': profile_form,
        }
        return render(request, 'forms/registration.html', context)

    def post(self, request, *args, **kwargs):
        u_name = request.POST.get('username')
        # print(request.POST ,'', request.FILES)
        profile_form = AuthorProfileForm(request.POST, request.FILES)
        form = CreateUserForm(request.POST)

        if profile_form.is_valid() and form.is_valid():
            user = form.save()
            username = user.username

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.uid = random_int()
            profile.save()
            staff = Author.objects.get(user=request.user)
            act = Activity(actor=staff, type='Add', action=f'Account created for {username}')
            act.save()

            messages.success(request, 'Account was created for ' + username)

            return redirect('store:s-home')

        else:
            # when the form has an error
            print(profile_form.errors)
            profile_form = AuthorProfileForm()
            messages.success(request, 'Fill out all the necessary details ')
            context = {
                'form': form,
                'profile_form': profile_form,
            }
            return render(request, 'forms/registration.html', context)


class DeleteStaff(LoginRequiredMixin, DeleteView):

    model = Author
    template_name = 'forms/delete_staff.html'
    success_url = reverse_lazy('store:s_home')


class AddProduct(LoginRequiredMixin, CreateView):

    model = Product
    form_class = ProductForm
    template_name = 'forms/product.html'
    success_url = reverse_lazy('store:s_home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        author = Author.objects.get(user=self.request.user)
        form = form.save(commit=False)
        form.product_id = random_int()
        form.author = author

        form.save()

        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Add', action=f'Product added: {form.title}')
        act.save()
        # messages.success(self.request, 'Post was successfully added')
        return redirect('store:s_home')

    def form_invalid(self, form, *args, **kwargs):
        # print(self.request.POST)
        # print(form.errors)
        # messages.success(self.request, 'Post was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/product.html', {'form': form})


class DeleteProduct(LoginRequiredMixin, DeleteView):

    model = Product
    template_name = 'forms/delete_product.html'
    slug_field = 'product_id'
    slug_url_kwarg = 'product_id'
    success_url = reverse_lazy('store:s_home')


class AddProductImage(LoginRequiredMixin, CreateView):

    model = ProductImage
    form_class = ProductImageForm
    template_name = 'forms/product-image.html'

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save(commit=False)
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Add', action=f'Product Image category added: {form.product}')
        act.save()
        if form.lead:
            print(self.object,':',form.product)
            try:
                old_lead = ProductImage.objects.get(product=form.product, lead=True)
                old_lead.lead = False
                old_lead.save()
                form.save()
                print('done')
            except:
                # form.save()
                pass
        # messages.success(self.request, 'Post category was successfully added')
        return redirect('store:product_images')

    def form_invalid(self, form, *args, **kwargs):
        print(form.errors)
        # messages.success(self.request, 'Post category was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/product-image.html', {'form': form})


class UpdateProductImage(LoginRequiredMixin, UpdateView):

    model = ProductImage
    form_class = ProductImageForm
    template_name = 'forms/update_product_img.html'
    success_url = reverse_lazy('store:s_home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save()
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Post image category updated: {form.title}')
        act.save()
        # messages.success(self.request, 'Post category was successfully updated')
        return redirect('content:s_home')


class DeleteProductImage(LoginRequiredMixin, DeleteView):

    model = ProductImage
    template_name = 'forms/delete_product_img.html'
    success_url = reverse_lazy('store:s_home')


class AddProductCat(LoginRequiredMixin, CreateView):

    model = ProductCategory
    form_class = ProductCatForm
    template_name = 'forms/post-cat.html'

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save()
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Add', action=f'Post category added: {form.name}')
        act.save()
        # messages.success(self.request, 'Post category was successfully added')
        return redirect('store:s_home')

    def form_invalid(self, form, *args, **kwargs):
        # messages.success(self.request, 'Post category was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/product-category.html', {'form': form})


class UpdateProductCat(LoginRequiredMixin, UpdateView):

    model = ProductCategory
    form_class = ProductCatForm
    template_name = 'forms/update_product_cat.html'
    success_url = reverse_lazy('store:s_home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save()
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Product category updated: {form.name}')
        act.save()
        # messages.success(self.request, 'Post category was successfully updated')
        return redirect('store:s_home')


class DeleteProductCat(LoginRequiredMixin, DeleteView):

    model = ProductCategory
    template_name = 'forms/delete_product_cat.html'
    success_url = reverse_lazy('store:s_home')


class AddSlide(LoginRequiredMixin, CreateView):

    model = Slide
    form_class = SlideForm
    template_name = 'forms/slide.html'
    success_url = reverse_lazy('store:s_home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save(commit=False)
        # print('index is :',form.index)
        if form.index is not None:
            slides = Slide.objects.all()
            d_max = max([ind.index for ind in slides])
            if form.index < d_max:
                for i in slides:
                    if i.index >= form.index:
                        i.index += 1
                        i.save()
        else:
            slides = Slide.objects.all()
            d_max = [index.index for index in slides]
            # print(d_max)
            d_max = max(d_max)
            form.index = d_max + 1
        form.save()

        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Add', action=f'Slide added: slide-{form.index}')
        act.save()
        # messages.success(self.request, 'Slide was successfully added')
        return redirect('store:s_home')

    def form_invalid(self, form, *args, **kwargs):
        # print(self.request.POST)
        # print(form.errors)
        # messages.success(self.request, 'Slide was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/slide.html', {'form': form})


class UpdateSlide(LoginRequiredMixin, UpdateView):

    model = Slide
    form_class = SlideForm
    template_name = 'forms/update_slide.html'
    success_url = reverse_lazy('store:s_home')

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save(commit=False)
        # print('index is :',form.index)
        if form.index is not None:
            if form.index != self.object.index:
                slides = Slide.objects.all()
                d_max = max([ind.index for ind in slides])
                if form.index < d_max:
                    for i in slides:
                        if i.index >= form.index:
                            i.index += 1
                            i.save()
        else:
            slides = Slide.objects.all()
            d_max = [index.index for index in slides]
            # print(d_max)
            d_max = max(d_max)
            form.index = d_max + 1
        if form.link == 'None':
            form.link = None
        form.save()

        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Slide updated: slide-{form.index}')
        act.save()
        # messages.success(self.request, 'Slide was successfully added')
        return redirect('store:s_home')


class DeleteSlide(LoginRequiredMixin, DeleteView):

    model = Slide
    template_name = 'forms/delete_slide.html'
    success_url = reverse_lazy('store:s_home')


class FirstnameUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = FirstnameChangeForm
    template_name = 'forms/firstname-update.html'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'first name updated for {self.object}')
        act.save()
        return reverse('store:staff_detail', kwargs={'uid': self.object.id})


class SurnameUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = SurnameChangeForm
    template_name = 'forms/surname-update.html'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Surname updated for {self.object}')
        act.save()
        return reverse('store:staff_detail', kwargs={'uid': self.object.id})

# ------------------------ Update Product -----------------------


class ProductNameUpdate(LoginRequiredMixin, UpdateView):

    model = Product
    form_class = ProductNameChangeForm
    template_name = 'forms/product_name_update.html'
    slug_field = 'product_id'
    slug_url_kwarg = 'product_id'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Name updated for {self.object}')
        act.save()
        return reverse('store:staff_product_detail', kwargs={'product_id': self.object.product_id})


class ProductCategoryUpdate(LoginRequiredMixin, UpdateView):

    model = Product
    form_class = ProductCategoryChangeForm
    template_name = 'forms/product_cat_update.html'
    slug_field = 'product_id'
    slug_url_kwarg = 'product_id'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Category updated for {self.object}')
        act.save()
        return reverse('store:staff_product_detail', kwargs={'product_id': self.object.product_id})

    def form_invalid(self, form, *args, **kwargs):
        # print(self.request.POST)
        print(form.errors)
        # messages.success(self.request, 'Slide was not added, ensure that you filled the form correctly')
        return render(self.request, 'forms/product_cat_update.html', {'form': form})


class ProductBrandUpdate(LoginRequiredMixin, UpdateView):

    model = Product
    form_class = ProductBrandChangeForm
    template_name = 'forms/product-brand-update.html'
    slug_field = 'product_id'
    slug_url_kwarg = 'product_id'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Product brand updated for {self.object}')
        act.save()
        return reverse('store:staff_product_detail', kwargs={'product_id': self.object.product_id})


class ProductColorsUpdate(LoginRequiredMixin, UpdateView):

    model = Product
    form_class = ProductColorsChangeForm
    template_name = 'forms/product-color-update.html'
    slug_field = 'product_id'
    slug_url_kwarg = 'product_id'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Product colors updated for {self.object}')
        act.save()
        return reverse('store:staff_product_detail', kwargs={'product_id': self.object.product_id})


class ProductSizesUpdate(LoginRequiredMixin, UpdateView):

    model = Product
    form_class = ProductSizesChangeForm
    template_name = 'forms/product-size-update.html'
    slug_field = 'product_id'
    slug_url_kwarg = 'product_id'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Product sizes updated for {self.object}')
        act.save()
        return reverse('store:staff_product_detail', kwargs={'product_id': self.object.product_id})


class ProductPriceUpdate(LoginRequiredMixin, UpdateView):

    model = Product
    form_class = ProductPriceChangeForm
    template_name = 'forms/product-price-update.html'
    slug_field = 'product_id'
    slug_url_kwarg = 'product_id'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Product price updated for {self.object}')
        act.save()
        return reverse('store:staff_product_detail', kwargs={'product_id': self.object.product_id})


class ProductDiscountPriceUpdate(LoginRequiredMixin, UpdateView):

    model = Product
    form_class = ProductDiscountPriceChangeForm
    template_name = 'forms/product_discount_price_update.html'
    slug_field = 'product_id'
    slug_url_kwarg = 'product_id'

    def get_success_url(self):
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Product colors updated for {self.object}')
        act.save()
        return reverse('store:staff_product_detail', kwargs={'product_id': self.object.product_id})


class ProductProductImageUpdate(LoginRequiredMixin, UpdateView):

    model = ProductImage
    form_class = ProductProductImageChangeForm
    template_name = 'forms/product_image_update.html'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def form_valid(self, form, *args, **kwargs):
        # print(self.request.POST)
        form = form.save(commit=False)
        staff = Author.objects.get(user=self.request.user)
        act = Activity(actor=staff, type='Update', action=f'Product image updated for {self.object}')
        act.save()
        if form.lead:
            print(self.object,':',form.product)
            try:
                old_lead = ProductImage.objects.get(product=form.product, lead=True)
                old_lead.lead = False
                old_lead.save()
                form.save()
                print('done')
            except:
                # form.save()
                pass
        # messages.success(self.request, 'Post category was successfully added')
        print(self.object.product.product_id)
        # return reverse('store:staff_product_detail', kwargs={'product_id': self.object.product.product_id })
        return redirect('store:s_home')

    # def get_success_url(self):
    #     return reverse('store:staff_product_detail', kwargs={'product_id': self.object.product_id})
