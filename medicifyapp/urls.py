from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('gp_jobs', views.gp_jobs, name='gp_jobs'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profile, name='profile'),
    path('my_order', views.my_order, name='my_order'),
    path('order_details', views.order_details, name='order_details'),
    path('post_job', views.post_job, name='post_job'),
    path('see_my_post', views.see_my_post, name='see_my_post'),
    path('job_post_details/<int:pk>', views.job_post_details, name='job_post_details'),
    path('product_search', views.product_search, name='product_search'),
    # path('category_search', views.category_search, name='category_search'),
    path('category_search_by_user/<int:pk>', views.category_search_by_user, name='category_search_by_user'),
    path('account', views.account, name='account'),
    path('login_func', views.login_func, name='login_func'),

    path('email/confirmation/<str:activation_key>/', views.email_confirm, name='email_activation'  ),

    path('func_logout', views.func_logout, name='func_logout'),
    path('cart', views.cart, name='cart'),
    path('details_products/pro-<int:pk>-all', views.details_products, name='details_products'),
    path('details_products/product_search', views.product_search, name='product_search'),
]
