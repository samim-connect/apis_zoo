from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
import uuid

# App level import
from .util import choice


class Category(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['title']


class SubCategory(models.Model):
    title = models.TextField()
    parent_category = models.ForeignKey(
        'Category', blank=True, null=True, related_name='parent_category')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Sub-Categories'
        ordering = ['title']


class Product(models.Model):
    title = models.TextField()
    description = models.TextField()
    seller = models.ForeignKey(
        'UserProfile', related_name='seller_name', blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    image_url = models.CharField(blank=True, null=True, max_length=1000)
    # shop = models.ForeignKey(
    #     'Shop', blank=True, null=True, related_name='shop_name')
    # reviews = models.ForeignKey('Review', blank=True, null=True)
    location = models.ForeignKey('Location', blank=True, null=True)
    in_stock = models.IntegerField(default=1, blank=True, null=True)
    category = models.ForeignKey(
        'SubCategory', blank=True, null=True, related_name='product_category')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Service(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    rate = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        'ServiceCategory', related_name='service_category')

    def __str__(self):
        return '{} from {}', format(self.service_name, self.category)

    class Metas:
        ordering = ['service_name']


class ServiceCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Location(models.Model):
    latitute = models.DecimalField(
        max_digits=65, decimal_places=30, default=Decimal(0.0000))
    longitute = models.DecimalField(
        max_digits=65, decimal_places=30, default=Decimal(0.0000))
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return 'The latitude is {} and longitute is {}'.format(
            self.latitute, self.longitute)


class Cart(models.Model):
    item_list = models.ManyToManyField('Product', blank=True)


class UserProfile(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    user_type = models.CharField(max_length=40, choices=choice.USER_TYPE)
    location = models.ForeignKey('Location', blank=True, null=True)
    seller_identity = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    cart = models.OneToOneField(
        'Cart', blank=True, null=True, related_name='users_cart')
    image = models.ImageField(blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']


class Review(models.Model):
    description = models.TextField()
    rating = models.IntegerField(default=0, null=True, blank=True)
    item = models.ForeignKey('Product', related_name='product_review')
    user = models.ForeignKey('UserProfile', related_name='reviewer')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return '{} commented - {}'.format(self.user, self.item)

    class Meta:
        ordering = ['user']


class Order(models.Model):
    customer_name = models.ForeignKey(
        'UserProfile', related_name='order_customer_name')
    item = models.ForeignKey('Product', related_name='order_product_name')
    seller_name = models.ForeignKey(
        'UserProfile', related_name='sellers_order')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return '{} has odered {} selling by {} on {}'.format(
            self.customer_name, self.item, self.seller_name, self.time)

    class Meta:
        ordering = ['timestamp']


class Carosal(models.Model):
    image = models.ImageField()
    link = models.CharField(max_length=400)

    def __str__(self):
        return self.link
