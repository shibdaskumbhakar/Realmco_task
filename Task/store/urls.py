
from django.contrib import admin
from django.urls import path, re_path
from store.views import home, cart, login, signup, logout, ProductDetailSlugViews, add_to_cart, admin


urlpatterns = [
    path('', home, name='home'),
    path('cart', cart),
    path('login/', login),
    path('custom-admin/', admin),
    path('signup/', signup),
    path('logout/', logout),

    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugViews.as_view()),

    path('addtocart/<str:slug>', add_to_cart),
    # path('staff_user/', admin),
]
