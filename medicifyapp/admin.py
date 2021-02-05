from django.contrib import admin
from .models import Product_Details, Categories, posted_jobs, job_post_status, Order, EmailConfirmed, bennar, contact_table

# Register your models here.


class EmailConfirmedAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'activation_key', 'email_confirmed']

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

admin.site.register(EmailConfirmed, EmailConfirmedAdmin)



class show_order(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'email', 'order_date']


admin.site.register(Product_Details)
admin.site.register(Categories)
admin.site.register(posted_jobs)
admin.site.register(job_post_status)
admin.site.register(Order, show_order)
admin.site.register(bennar)
admin.site.register(contact_table)