from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product_Details, Categories, posted_jobs, job_post_status, Order, bennar, contact_table
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .models import EmailConfirmed
from django.shortcuts import get_object_or_404
# Create your views here.


def index(request):
    Product_Details_all = Product_Details.objects.all().order_by('-id')

    # send_mail(
    #     'Purchase Order',  # subject
    #     'email_for_buy',  # massage
    #     '',  # from email
    #     ['abdurrahmanchowdhury1122@gmail.com'],  # to email
    #
    #     fail_silently=True,
    # )

    # pagination
    p = Paginator(Product_Details_all, 15)
    # print(p.num_pages)
    number_of_pages = p.num_pages

    #show list of pages
    number_of_pages_1 = p.num_pages+1
    list = []
    for i in range(1, number_of_pages_1):
        list.append(i)

    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    Categories_all = Categories.objects.all()

    # Search_with_price_all = Search_with_price.objects.all()
    # print(Search_with_price_all)

    # query jobs
    all_jobs = posted_jobs.objects.filter(job_post_status='2').order_by('-id')
    p_jobs = Paginator(all_jobs, 4)
    page2 = p_jobs.page(1)

    # if not price2:
    #     price2 = Add_prod.objects.aggregate(Max('price'))['price__max']
    #
    # my_products = Add_prod.objects.filter(price__range=(price1, price2))


    bennar_first = bennar.objects.first()

    get_id_benner=bennar_first.id

    bennar_all = bennar.objects.all().exclude(id=get_id_benner)

    context2 = {'Product_Details_all':page, 'Categories_all':Categories_all, 'list':list, 'all_jobs':page2, 'page_num':page_num, 'bennar_all':bennar_all, 'bennar_first':bennar_first}
    return render(request, 'index.html', context2)



def profile(request):
    Categories_all = Categories.objects.all()
    context22= {'Categories_all':Categories_all}
    return render(request, 'profile.html', context22)


def gp_jobs(request):
    if request.method == "POST":
        job_title = request.POST.get('job_title')
        job_location = request.POST.get('job_location')
        job_type = request.POST.get('job_type')
        # print(job_title, job_location, job_type)


        # search_jobs_form = posted_jobs.objects.filter(Q(job_title__icontains=job_title) | Q(job_details__icontains=job_title) | Q(job_location__icontains=job_location) | Q(job_type__icontains=job_type)).order_by('-id')

        search_jobs_form = posted_jobs.objects.filter(Q(job_title__icontains=job_title) | Q(job_details__icontains=job_title)).filter(job_post_status='2').order_by('-id')

        search_jobs_count = posted_jobs.objects.filter(Q(job_title__icontains=job_title) | Q(job_details__icontains=job_title)).filter(job_post_status='2').order_by('-id').count()

        Categories_all = Categories.objects.all()

        context13 = {'search_jobs_form':search_jobs_form, 'job_title':job_title, 'job_location':job_location, 'job_type':job_type, 'search_jobs_count':search_jobs_count, 'Categories_all':Categories_all}
        return render(request, 'gp_jobs.html', context13)
    else:
        all_job_post = posted_jobs.objects.filter(job_post_status='2').order_by('-id')
        Categories_all = Categories.objects.all()
        context12 = {'all_job_post':all_job_post, 'Categories_all':Categories_all}
        return render(request, 'gp_jobs.html', context12)

def contact(request):
    name=request.POST.get('name')
    email=request.POST.get('email')
    message=request.POST.get('message')

    save_contact_table=contact_table(name=name, email=email, message=message)
    save_contact_table.save()

    messages.success(request, name+' Your Message Successfully Deliver to Manager. Our manager will get back to you soon. Thank You !!')
    return redirect('/')



def about(request):
    Categories_all = Categories.objects.all()
    context22 = {'Categories_all': Categories_all}
    return render(request, 'about.html', context22)


def see_my_post(request):
    user = request.user
    mypost = posted_jobs.objects.filter(user=user).order_by('-id')

    # pagination
    p = Paginator(mypost, 10)
    # print(p.num_pages)
    number_of_pages = p.num_pages

    # show list of pages
    number_of_pages_1 = p.num_pages + 1
    list = []
    for i in range(1, number_of_pages_1):
        list.append(i)

    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    Categories_all = Categories.objects.all()

    context11 = {'mypost':page, 'list':list, 'Categories_all':Categories_all}
    return render(request, 'see_my_post.html', context11)


def job_post_details(request, pk):
    get_posted_jobs_id = posted_jobs.objects.get(id=pk)
    Categories_all = Categories.objects.all()

    context11 = {'get_posted_jobs_id':get_posted_jobs_id, 'Categories_all':Categories_all}
    return render(request, 'job_post_details.html', context11)

def post_job(request):
    if request.method=="POST":
        post_job_title1 = request.POST.get('post_job_title', '')
        # a=post_job_title.capitalize()
        post_job_title=post_job_title1.upper()

        post_job_details = request.POST.get('post_job_details', '')

        post_job_location1 = request.POST.get('post_job_location', '')
        post_job_location = post_job_location1.upper()

        post_job_type = request.POST.get('post_job_type', '')
        jobs_salary = request.POST.get('jobs_salary', '')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        company_name = request.POST.get('company_name', '')
        qualification = request.POST.get('qualification', '')

        job_p_status = request.POST.get('job_p_status')
        # print(job_p_status)

        het_job_pst_sttus = job_post_status.objects.get(job_post_status=job_p_status)

        user = request.user
        # print(user)

        save_job_post = posted_jobs(user=user, job_title=post_job_title, company_name=company_name, job_details=post_job_details, qualification=qualification, job_location=post_job_location, job_type=post_job_type, salary=jobs_salary, phone_number=phone_number, job_post_status=het_job_pst_sttus, email=email)
        save_job_post.save()

        messages.success(request, 'Your Job Post is Under Review !! If Every Thing Alright, Your post will be Arrived in 48 hours !!')

        return redirect('gp_jobs')
    else:
        get_status = job_post_status.objects.filter(id='1')
        Categories_all = Categories.objects.all()

        context10 = {'get_status': get_status, 'Categories_all':Categories_all}
        return render(request, 'post_job.html', context10)


def product_search(request):
    search_product  = request.GET.get('search_product')

    # prod_search = Product_Details.objects.filter(product_name__icontains = search_product)
    # prod_search_des = Product_Details.objects.filter(description__icontains = search_product)
    #
    # search_result = prod_search.union(prod_search_des)

    if search_product:
        search_result = Product_Details.objects.filter(Q(product_name__icontains = search_product) | Q(description__icontains = search_product)).order_by('-id')

        search_result_count = Product_Details.objects.filter(Q(product_name__icontains = search_product) | Q(description__icontains = search_product)).count()

    # pagination
    p = Paginator(search_result, 15)

    # print(p.num_pages)
    number_of_pages = p.num_pages

    # show list of pages in template
    number_of_pages_1 = p.num_pages + 1
    list1 = []
    for i in range(1, number_of_pages_1):
        list1.append(i)

    page_num = request.GET.get('page', 1)
    print(page_num)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    Categories_all = Categories.objects.all()
    # Search_with_price_all = Search_with_price.objects.all()

    # query jobs
    all_jobs = posted_jobs.objects.filter(job_post_status='2').order_by('-id')
    p_jobs = Paginator(all_jobs, 4)
    page2 = p_jobs.page(1)


    context5 = {'Product_Details_all':page, 'search_product':search_product, 'Categories_all':Categories_all, 'search_result_count':search_result_count, 'list1':list1, 'all_jobs':page2}
    return render(request, 'index.html', context5)


def category_search_by_user(request, pk):
    get_all_prod_by_cat = Product_Details.objects.filter(category=pk).order_by('-id')

    # pagination
    p = Paginator(get_all_prod_by_cat, 15)
    # print(p.num_pages)
    number_of_pages = p.num_pages

    # show list of pages
    number_of_pages_1 = p.num_pages + 1
    list = []
    for i in range(1, number_of_pages_1):
        list.append(i)

    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    Categories_all = Categories.objects.all()

    # query jobs
    all_jobs = posted_jobs.objects.filter(job_post_status='2').order_by('-id')
    p_jobs = Paginator(all_jobs, 4)
    page2 = p_jobs.page(1)

    context={'Product_Details_all':page, 'list':list, 'Categories_all':Categories_all, 'all_jobs':page2}
    return render(request, 'index.html', context)



#
# def category_search(request):
#     checkbox_cat_seach = request.GET.get('checkbox_cat_seach')
#     price_search_check = request.GET.get('price_search_check')
#
#     if checkbox_cat_seach and price_search_check:
#         cat_details_get = Categories.objects.get(id=checkbox_cat_seach)
#         # price_details_get = Search_with_price.objects.get(id=price_search_check)
#
#         get_minmum_price = price_details_get.minimum_price
#         get_maximum_price=price_details_get.maximum_price
#
#         get_all_prod_by_cat = Product_Details.objects.filter(category=cat_details_get).order_by('-id').filter(price__gte=get_minmum_price).filter(price__lte=get_maximum_price)
#         # print(get_all_prod_by_cat)
#
#         get_all_prod_by_cat2 = Product_Details.objects.filter(category=cat_details_get).order_by('-id').filter(
#             price__gte=get_minmum_price).filter(price__lte=get_maximum_price).count()
#
#         # pagination
#         p = Paginator(get_all_prod_by_cat, 15)
#
#         # print(p.num_pages)
#         number_of_pages = p.num_pages
#
#         # show list of pages in template
#         number_of_pages_1 = p.num_pages + 1
#         list2 = []
#         for i in range(1, number_of_pages_1):
#             list2.append(i)
#
#         page_num = request.GET.get('page', 1)
#         try:
#             page = p.page(page_num)
#         except EmptyPage:
#             page = p.page(1)
#
#         Categories_all = Categories.objects.all()
#         Search_with_price_all = Search_with_price.objects.all()
#
#         # query jobs
#         all_jobs = posted_jobs.objects.filter(job_post_status='2').order_by('-id')
#         p_jobs = Paginator(all_jobs, 10)
#         page2 = p_jobs.page(1)
#
#         context8 = {'Categories_all': Categories_all, 'Product_Details_all': page, 'get_all_prod_by_cat2': get_all_prod_by_cat2, 'cat_details_get': cat_details_get, 'Search_with_price_all':Search_with_price_all, 'price_details_get':price_details_get, 'list2':list2, 'all_jobs':page2}
#
#         return render(request, 'index.html', context8)
#
#     elif checkbox_cat_seach:
#         cat_details_get = Categories.objects.get(id=checkbox_cat_seach)
#         # print(checkbox_cat_seach)
#         get_all_prod_by_cat = Product_Details.objects.filter(category=cat_details_get).order_by('-id')
#         get_all_prod_by_cat2 = Product_Details.objects.filter(category=cat_details_get).count()
#         # print(get_all_prod_by_cat)
#
#         # pagination
#         p = Paginator(get_all_prod_by_cat, 15)
#
#         # print(p.num_pages)
#         number_of_pages = p.num_pages
#
#         # show list of pages in template
#         number_of_pages_1 = p.num_pages + 1
#         list2 = []
#         for i in range(1, number_of_pages_1):
#             list2.append(i)
#
#         page_num = request.GET.get('page', 1)
#         try:
#             page = p.page(page_num)
#         except EmptyPage:
#             page = p.page(1)
#
#
#         Categories_all = Categories.objects.all()
#         Search_with_price_all = Search_with_price.objects.all()
#
#         # query jobs
#         all_jobs = posted_jobs.objects.filter(job_post_status='2').order_by('-id')
#         p_jobs = Paginator(all_jobs, 10)
#         page2 = p_jobs.page(1)
#
#
#         context5 = {'Categories_all': Categories_all, 'Product_Details_all': page,
#                             'get_all_prod_by_cat2': get_all_prod_by_cat2, 'cat_details_get': cat_details_get, 'Search_with_price_all':Search_with_price_all, 'list2':list2, 'all_jobs':page2}
#         return render(request, 'index.html', context5)
#
#     elif price_search_check:
#         price_details_get = Search_with_price.objects.get(id=price_search_check)
#         # print(checkbox_cat_seach)
#
#         get_minmum_price = price_details_get.minimum_price
#         get_maximum_price = price_details_get.maximum_price
#         # print(get_minmum_price, get_maximum_price)
#
#         # price_searching = Product_Details.objects.filter(price__gte=get_minmum_price).filter(
#         #     price__lte=get_maximum_price)
#         # print(price_searching)
#
#         get_all_prod_by_cat = Product_Details.objects.filter(price__gte=get_minmum_price).filter(
#             price__lte=get_maximum_price)
#         get_all_prod_by_cat2 = Product_Details.objects.filter(price__gte=get_minmum_price).filter(
#             price__lte=get_maximum_price).count()
#
#         # pagination
#         p = Paginator(get_all_prod_by_cat, 15)
#
#         # print(p.num_pages)
#         number_of_pages = p.num_pages
#
#         # show list of pages in template
#         number_of_pages_1 = p.num_pages + 1
#         list2 = []
#         for i in range(1, number_of_pages_1):
#             list2.append(i)
#
#         page_num = request.GET.get('page', 1)
#         try:
#             page = p.page(page_num)
#         except EmptyPage:
#             page = p.page(1)
#
#         Categories_all = Categories.objects.all()
#         Search_with_price_all = Search_with_price.objects.all()
#
#         # query jobs
#         all_jobs = posted_jobs.objects.filter(job_post_status='2').order_by('-id')
#         p_jobs = Paginator(all_jobs, 10)
#         page2 = p_jobs.page(1)
#
#         context6 = {'Categories_all':Categories_all, 'Search_with_price_all':Search_with_price_all, 'Product_Details_all':page, 'get_all_prod_by_cat2':get_all_prod_by_cat2, 'price_details_get':price_details_get, 'list2':list2, 'all_jobs':page2}
#         return render(request, 'index.html', context6)
#
#     else:
#         return redirect('/')


def account(request):
    if request.method=='POST':

        #check the post peramiters
        sign_username=request.POST['sign_username']
        sign_email=request.POST['sign_email']
        sign_password=request.POST['sign_password']
        confirm_sign_password=request.POST['confirm_sign_password']
        sign_first_name=request.POST['sign_first_name']
        sign_last_name=request.POST['sign_last_name']




        #chech the error inputs

        user_username_info = User.objects.filter(username=sign_username)
        user_email_info = User.objects.filter(email=sign_email)

        erorr_message= ""

        if user_username_info:
            # messages.error(request, "Username Already Exist")
            erorr_message = "Username Already Exist"

        elif user_email_info:
            # messages.error(request, "Email Already Exist")
            erorr_message = "Email Already Exist"

        elif sign_password != confirm_sign_password:
            # messages.error(request, "Passwords are not match")
            erorr_message = "Passwords are not match"

        elif len(sign_password)<7:
            # messages.error(request, "Passwords Must be Al least 7 Digits")
            erorr_message = "Passwords Must be Al least 7 Digits"

        if not erorr_message:

            # create user
            myuser = User.objects.create_user(sign_username, sign_email, sign_password)
            myuser.first_name=sign_first_name
            myuser.last_name=sign_last_name
            myuser.is_active = False
            myuser.save()


            # send mail
            user = EmailConfirmed.objects.get(user=myuser)
            site = get_current_site(request)
            email = myuser.email
            first_name = myuser.first_name
            last_name = myuser.last_name

            sub_of_email = "Activation Email From Medicify."
            email_body = render_to_string(
                'verify_email.html',
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'domain': site.domain,
                    'activation_key': user.activation_key
                }
            )

            send_mail(
                sub_of_email,  # Subject of message
                email_body,  # Message
                '',  # From Email
                [email],  # To Email

                fail_silently=True
            )

            messages.success(request, 'Check Your Email for Activate Your Account !!!')

            return redirect('/')

        else:
            Categories_all = Categories.objects.all()

            value_dic = {'sign_username': sign_username, 'sign_email': sign_email, 'sign_first_name': sign_first_name,
                         'sign_last_name': sign_last_name, 'erorr_message':erorr_message, 'Categories_all':Categories_all}
            return render(request, 'account.html', value_dic)

    else:
        usr = request.user
        # print(usr)
        user_username = User.objects.filter(username=usr)
        # print(user_username)
        if user_username:
            return redirect('/')
        else:
            Categories_all = Categories.objects.all()
            condict = {'Categories_all':Categories_all}
            return render(request, 'account.html', condict)



def email_confirm(request, activation_key):
    user= get_object_or_404(EmailConfirmed, activation_key=activation_key)
    if user is not None:
        user.email_confirmed=True
        user.save()

        myuser=User.objects.get(email=user)
        myuser.is_active=True
        myuser.save()

        Categories_all = Categories.objects.all()
        condict = {'Categories_all': Categories_all}
        return render(request, 'registration_complete.html', condict)





def login_func(request):
    if request.method == 'POST':
        log_username = request.POST['log_username']
        log_password = request.POST['log_password']
        # this is for authenticate username and password for login
        user = authenticate(username=log_username, password=log_password)

        erorr_message_2 = ""

        if user is not None:
            login(request, user)
            # messages.success(request, "Successfully Logged In !!")
            return redirect('index')
        else:
            erorr_message_2 ="Invalid Credentials, Please Try Again !!"

            Categories_all = Categories.objects.all()

            value_func2 = {'erorr_message_2':erorr_message_2, 'log_username':log_username, 'Categories_all':Categories_all}
            # messages.error(request, "Invalid Credentials, Please Try Again !!")
            return render(request, 'account.html', value_func2)


def func_logout(request):
    # this is for logout from user id
    logout(request)
    return redirect('index')


def details_products(request, pk):
    Product_Details_details= Product_Details.objects.get(id=pk)
    # print(Product_Details_details.category)

    Product_Details_details_category=Product_Details_details.category

    Product_Details_by_cate = Product_Details.objects.filter(category=Product_Details_details_category).order_by('-id')

    Categories_all = Categories.objects.all()

    context3 = {'Product_Details_details':Product_Details_details, 'Product_Details_by_cate':Product_Details_by_cate, 'Categories_all':Categories_all}
    return render(request, 'products_details.html', context3)

def cart(request):
    if request.method =="POST":

        items_json=request.POST.get('items_json')

        all_prod=request.POST.get('all_prod')
        all_prod_price=request.POST.get('all_prod_price')
        all_prod_qty=request.POST.get('all_prod_qty')
        prod_details=request.POST.get('prod_details')

        # print(prod_details)


        total_bill=request.POST.get('total_bill')

        company_name=request.POST.get('company_name')
        full_address=request.POST.get('full_address')
        city=request.POST.get('city')
        postal_code=request.POST.get('postal_code')
        country=request.POST.get('country')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        # print(full_address, city, postal_code, country, phone)

        #make random order ID
        random_num = random.randint(2345678909800, 9923456789000)

        uniqe_confirm = Order.objects.filter(order_id=random_num)
        # print(random_num)

        while uniqe_confirm:
            random_num = random.randint(234567890980000, 992345678900000)
            if not Order.objects.filter(order_id=random_num):
                break
        # print(random_num)



        user = request.user

        post_order = Order(user=user, order_id=random_num, items_json=prod_details, total_bill=total_bill,  company_name=company_name, full_address=full_address, city=city, postal_code=postal_code, country=country, phone=phone, email=email)
        post_order.save()
        order_id = post_order.order_id
        # print(order_id)


        email_for_buy = render_to_string(
            'email_for_buy.html',
            {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'prod_details': prod_details,
                'total_bill': total_bill,
                'full_address' :full_address,
                'city' : city,
                'postal_code' :postal_code,
                'country' : country,
                'phone' : phone,
                'email' : email,
            }
        )

        send_mail(
            'Purchase Order',  # subject
            email_for_buy,  # massage
            '',  # from email
            [email],  # to email

            fail_silently=True,
        )

        email_for_admin = render_to_string(
            'email_for_admin.html',
            {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'prod_details': prod_details,
                'total_bill': total_bill,
                'full_address': full_address,
                'city': city,
                'postal_code': postal_code,
                'country': country,
                'phone': phone,
                'email': email,
            }
        )

        send_mail(
            'Received a Order',  # subject
            email_for_admin,  # massage
            '',  # from email
            [''],  # to email

            fail_silently=True,
        )
        # print("come")

        Thank = True
        Categories_all = Categories.objects.all()
        return render(request, 'cart.html', {'Thank':Thank, 'order_id':order_id, 'Categories_all':Categories_all})

    Categories_all = Categories.objects.all()
    dict={'Categories_all':Categories_all}
    return render(request, 'cart.html', dict)

def my_order(request):
    user = request.user

    # print(usr)
    user_username = User.objects.filter(username=user)
    # print(user_username)
    if user_username:
        myorder_filter = Order.objects.filter(user=user).order_by('-id')
        Categories_all = Categories.objects.all()
        context13 = {'myorder_filter': myorder_filter, 'Categories_all':Categories_all}
        return render(request, 'my_order.html', context13)
    else:
        return redirect('/')




def order_details(request):
    if request.method=="POST":
        user = request.user
        order_id=request.POST.get('order_id')
        print(order_id, user)
        myorder_details = Order.objects.get(id=order_id)

        dict1=myorder_details.items_json


        # using zip()
        # list1, list2 = list(zip(*dict1.items()))

        # list1=[]
        # list2=[]
        #
        # #using items()
        # for i in dict1.items():
        #     list1.append(i[0]), list2.append(i(1))
        #
        # print(dict1)

        Categories_all = Categories.objects.all()

        context13 = {'myorder_details':myorder_details, 'Categories_all':Categories_all}
        return render(request, 'order_details.html', context13)
    else:
        return redirect('/')

