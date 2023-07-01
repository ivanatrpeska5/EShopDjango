"""
URL configuration for EShopDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from EShopDjango import settings
from MobileXpress.views import login_view, register_view, store, details, home, logout_view, add_to_cart, shopping_cart, \
    order_form, order_details, payment_form, successful_order, my_orders, cancel_order, finished_order, admin_orders, \
    in_delivery_order, profile, about_us, add_product, delete_product, successful_delete_product, delete_from_cart

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('login/', login_view, name="login"),
                  path('register/', register_view, name="register"),
                  path('store/', store, name="store"),
                  path('about_us/', about_us, name="about_us"),
                  path('details/<int:pk>/', details, name="details"),
                  path('', home, name="home"),
                  path('logout/', logout_view, name="logout"),
                  path('add_to_cart/<int:pk>', add_to_cart, name="add_to_cart"),
                  path('shopping_cart/', shopping_cart, name="shopping_cart"),
                  path('order_form/', order_form, name="order_form"),
                  path('order_details/<int:pk>', order_details, name="order_details"),
                  path('payment_form/<int:pk>', payment_form, name="payment_form"),
                  path('successful_order', successful_order, name="successful_order"),
                  path('my_orders', my_orders, name="my_orders"),
                  path('admin_orders', admin_orders, name="admin_orders"),
                  path('cancel_order/<int:pk>', cancel_order, name="cancel_order"),
                  path('finished_order/<int:pk>', finished_order, name="finished_order"),
                  path('in_delivery_order/<int:pk>', in_delivery_order, name="in_delivery_order"),
                  path('profile/', profile, name="profile"),
                  path('add_product/', add_product, name="add_product"),
                  path('delete_product/<int:pk>', delete_product, name="delete_product"),
                  path('successful_delete_product', successful_delete_product, name="successful_delete_product"),
                  path('delete_from_cart/<int:pk>', delete_from_cart, name="delete_from_cart")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
