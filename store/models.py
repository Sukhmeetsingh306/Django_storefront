from uuid import uuid4
from django.contrib import admin
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

# this class is created as per the definition class as the product as this is the main class
# on which the other classes will depend #


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL,  null=True, related_name='+')
    # wrap the class name in '' to reduce the error of  circular productions
    # + will solve the reverse name relationship

    def __str__(self) -> str:
        return self.title

    class Meta:
        # this is made to sort the data according to the title
        ordering = ['title']


class Product(models.Model):
    # this will store the title in the string form
    title = models.CharField(max_length=255)
    slug = models.SlugField()  # going to add default value in terminal
    description = models.TextField(null=True, blank=True)  # just like the java
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)
    # as many to  many create the reverse relationship and
    # if we want to change the name that will be displayed we just have to add the related_name #

    def __str__(self) -> str:
        return self.title


class Customer(models.Model):
    # the data in the caps_locks that data is said to be included in this class only
    # as this object can't be called in other py#
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    # remove these as they are now made in the user.model
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    # adding another class name Meta

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    # (user) add as now they will respond from the user.model

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        # where there is need of this it will get on ot own
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history'),
        ]


class Order(models.Model):
    # the data in the caps_locks that data is said to be included in this class only
    # as this object can't be called in other py#
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    # protect will save the order history to be deleted if the customer got deleted

    class Meta:
        permissions = [
            ('cancel_order', 'Can Cancel Order')
        ]


class OrderItem(models.Model):
    # as this class have the order class as the foreignkey so the django will automatically
    # create a reverse relationship in both the classes as per django will create the
    # orderItem_set in the order class
    # but if we want to create a our own name field in that class we can use related name
    # but it will create a program in the code  #
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    # this will prevent the negative value
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # customer = models.OneToOneField(
    #     Customer, on_delete=models.CASCADE, primary_key=True)
    # as onetooneField relationship is the one that will be use to connect to class database
    # as the two class entires will be joined together as to work together as which parent class
    # will delete the data with it the child class data will be deleted
    # primary key is used so the database don't create a tuple of its own to identify the field]
    # as in this one customer cam have one address at a time as to add multiple address we
    # have to use the foreign key#
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    # this is one to  many relationship


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
