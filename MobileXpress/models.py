from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile/', blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='colors/', blank=True, null=True)

    def __str__(self):
        return self.name


class Phone(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    phone = models.ImageField(upload_to='photos/', blank=True, null=True)
    price = models.IntegerField()
    technology = models.CharField(max_length=255)
    dimensions = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    chipset = models.CharField(max_length=255)
    CPU = models.CharField(max_length=255)
    GPU = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)
    main_camera = models.CharField(max_length=255)
    front_camera = models.CharField(max_length=255)
    battery = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"


class PhoneColorQuantity(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.phone.name} - {self.color.name}: {self.quantity}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)

    def __str__(self):
        return self.phone.name

    def subtotal(self):
        return self.phone.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100,
                                    choices=(
                                        [('Created', 'Created'), ('InDelivery', 'InDelivery'),
                                         ('Finished', 'Finished')]))
    full_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100, choices=([('On Delivery', 'On Delivery'), ('Card', 'Card')]))

    def __str__(self):
        return str(self.id)


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=100,
                                 choices=(
                                     [('Visa', 'Visa'), ('MasterCard', 'MasterCard')]))
    card_number = models.CharField(max_length=255)
    exp_mm = models.IntegerField()
    exp_yy = models.IntegerField()
    security_code = models.IntegerField()
    card_holder_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)
