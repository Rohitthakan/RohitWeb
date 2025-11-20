from django.shortcuts import render, redirect
from home.models import Blog
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
# import dns.resolver
import random
import requests
import re

# Create your views here.
def index (request):
    blogs = Blog.objects.all()
    # random_blogs = random.sample(list(blogs), 3)
    blogs_list = list(blogs)
    sample_size = min(len(blogs_list), 3)  # don’t sample more than available
    random_blogs = random.sample(blogs_list, sample_size)
    context = {'random_blogs': random_blogs}
    return render(request, 'index.html', context)

def about (request):
    return render(request, 'about.html')

def verify_email_with_abstract(email):
    api_url = f"https://emailvalidation.abstractapi.com/v1/?api_key=e7b9d4e88c1141948d891902406fe70a&email={email}"
    response = requests.get(api_url)
    result = response.json()
    return result.get('deliverability') == 'DELIVERABLE', result

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')
        
        invalid_input = ['', ' ']
        
        if name in invalid_input or email in invalid_input or message in invalid_input:
            messages.error(request, 'One or more fields are empty!')
        else:
            email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            phone_pattern = re.compile(r'^(?:\+91|0)?[0-9]{10}$')
            
            if email_pattern.match(email) and (not phone or phone_pattern.match(phone)):
                email_exists, email_result = verify_email_with_abstract(email)
                
                if email_exists:
                    form_data = {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'message': message,
                    }
                    
                    message_body = '''
                    From:\n\t\t{}\n
                    Message:\n\t\t{}\n
                    Email:\n\t\t{}\n
                    Phone:\n\t\t{}\n
                    '''.format(form_data['name'], form_data['message'], form_data['email'], form_data['phone'])
                    
                    try:
                        send_mail('You got a mail from your portfolio website!', message_body, 'collegerepo2023@gmail.com', ['collegerepo2023@gmail.com'])
                        messages.success(request, 'Your message was sent.')
                    except:
                        messages.error(request, 'Failed to send email. Please try again later.')
                else:
                    messages.error(request, 'Email address does not exist!')
                    print(f"Email validation result: {email_result}")
            else:
                messages.error(request, 'Email or Phone is Invalid!')
    
    return render(request, 'contact.html', {})

def projects (request):
    return render(request, 'projects.html')

def blog(request):
    blogs = Blog.objects.all().order_by('-time')
    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    context = {'blogs': blogs}
    return render(request, 'blog.html', context)

def category(request, category):
    category_posts = Blog.objects.filter(category=category).order_by('-time')
    if not category_posts:
        message = f"No posts found in category: '{category}'"
        return render(request, "category.html", {"message": message})
    paginator = Paginator(category_posts, 3)
    page = request.GET.get('page')
    category_posts = paginator.get_page(page)
    return render(request, "category.html", {"category": category, 'category_posts': category_posts})

def categories(request):
    all_categories = Blog.objects.values('category').distinct().order_by('category')
    return render(request, "categories.html", {'all_categories': all_categories})


def blogpost (request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
        context = {'blog': blog}
        return render(request, 'blogpost.html', context)
    except Blog.DoesNotExist:
        context = {'message': 'Blog post not found'}
        return render(request, '404.html', context, status=404)


from django.http import FileResponse, HttpResponseForbidden
from django.conf import settings
import os

def backup_db_view(request):
    token = request.GET.get("token")
    SECRET_TOKEN = os.environ.get("DB_DOWNLOAD_TOKEN")  # put this in Render env

    if token != SECRET_TOKEN:
        return HttpResponseForbidden("Unauthorized")

    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    return FileResponse(open(db_path, 'rb'), as_attachment=True, filename='db.sqlite3')
