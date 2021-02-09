from django.db import models
from django.db.models.signals import pre_save
from store.utils import unique_slug_generator
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, unique=True)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='store/images', null=True, blank=True)

    def get_absolute_url(self):
        return "/{slug}/".format(slug=self.slug)

    def __str__(self):
        return self.title


def product_pre_save_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_reciver, sender=Product)


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quentity = models.IntegerField(default=1)
