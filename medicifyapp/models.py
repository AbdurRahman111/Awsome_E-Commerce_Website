from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
# Create your models here.


class EmailConfirmed(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key=models.CharField(max_length=500)
    email_confirmed=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural='User Email-Confirmed'

@receiver(post_save, sender=User)
def create_user_email_confirmation(sender, instance, created, **kwargs):
    if created:
        dt=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        email_confirmed_instance=EmailConfirmed(user=instance)
        user_encoded=f'{instance.email}-{dt}'.encode()
        activation_key=hashlib.sha224(user_encoded).hexdigest()
        email_confirmed_instance.activation_key=activation_key
        email_confirmed_instance.save()





class Categories(models.Model):
    category_name=models.CharField(max_length=500)

    def __str__(self):
        return self.category_name

class Product_Details(models.Model):
    product_name = models.CharField(max_length=500)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price = models.CharField(max_length=500)
    currency_type = models.CharField(max_length=1000, default='')
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/product_image', null=True, blank=True, default='')
    image2 = models.ImageField(upload_to='uploads/product_image', null=True, blank=True, default='')
    image3 = models.ImageField(upload_to='uploads/product_image', null=True, blank=True, default='')
    image4 = models.ImageField(upload_to='uploads/product_image', null=True, blank=True, default='')
    image5 = models.ImageField(upload_to='uploads/product_image', null=True, blank=True, default='')
    status = models.CharField(max_length=500)

    def __str__(self):
        return self.product_name + " " +self.price


class contact_table(models.Model):
    name=models.CharField(max_length=1000)
    email=models.CharField(max_length=1000)
    message=models.TextField()

    def __str__(self):
        return self.name


class job_post_status(models.Model):
    job_post_status=models.CharField(max_length=1000)

    def __str__(self):
        return self.job_post_status


class posted_jobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=1000, blank=True)
    company_name=models.CharField(max_length=1000, default='', blank=True)
    job_details = models.TextField(blank=True)
    qualification = models.CharField(max_length=1000, default='', blank=True)
    job_location = models.CharField(max_length=1000, blank=True)
    job_type = models.CharField(max_length=100, blank=True)
    salary = models.CharField(max_length=1000, blank=True)
    phone_number = models.CharField(max_length=1000, blank=True)
    job_post_status = models.ForeignKey(job_post_status, on_delete=models.CASCADE)
    post_date=models.DateField(default=datetime.now(), blank=True)
    email = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.user.username+" - "+self.job_title+" - "+self.salary+" - "+self.job_post_status.job_post_status


class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=1000)
    items_json = models.TextField()
    total_bill = models.CharField(max_length=1000)
    company_name=models.CharField(max_length=1000, default='', blank=True, null=True)
    full_address = models.TextField()
    city = models.CharField(max_length=1000)
    postal_code = models.CharField(max_length=100)
    country = models.CharField(max_length=1000)
    phone = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    order_date = models.DateField(default=datetime.now(), blank=True)
    

    # def __str__(self):
    #     return self.user.username + ' - '+self.company_name+ ' - '+self.email+ ' - '

class bennar(models.Model):
    name = models.CharField(max_length=10000)
    image = models.ImageField(upload_to='uploads/product_image')

    def __str__(self):
        return self.name