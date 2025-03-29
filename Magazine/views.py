from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from Magazine.models import Magazine, Comment, Subscriber, Contact_Us
from Magazine.forms import CommentForm, SubscriptionForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import User



# Create your views here.




def home(request):
    query = request.GET.get('q')  # Get search query from the request

    if request.method == "POST":

        email=request.POST.get('email')
        contact=Subscriber(email=email)
        contact.save()
        return redirect('/')

    if query:
        # Filter magazines by title or content based on search query
        latest_magazines = Magazine.objects.filter(title__icontains=query, is_published=True).order_by('-published_at')[:3]
        recent = Magazine.objects.filter(title__icontains=query, is_published=True).order_by('-published_at')[:5]
        old_magazines = Magazine.objects.filter(title__icontains=query, is_published=True).order_by('-published_at')[3:]

    else:
        # Default query when no search is performed
        most_popular = Magazine.objects.filter(is_published=True).order_by('-published_at')[:1]
        latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:3]
        latest_magazines_3_5 = Magazine.objects.filter(is_published=True).order_by('-published_at')[3:5]
        latest_magazines_5_8 = Magazine.objects.filter(is_published=True).order_by('-published_at')[5:8]
        recent = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
        old_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[3:]
        slider = Magazine.objects.filter(is_published=True).order_by('-published_at')[5:]


    context = {
        "latest_magazines": latest_magazines,
        "old_magazines": old_magazines,
        "recent": recent,
        "query": query,  # Pass query back to template to show in search field
        "latest_magazines_3_5": latest_magazines_3_5,
        "latest_magazines_5_8": latest_magazines_5_8,
        'most_popular':most_popular,
        'slider':slider,
    }
    return render(request, "home.html", context)



# List all published magazines
def magazine_list(request):

    most_popular_list = Magazine.objects.filter(is_published=True).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(is_published=True).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(is_published=True).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(is_published=True).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(is_published=True).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(is_published=True).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(is_published=True).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'magazine_list.html', context)




def magazine_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'magazine.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })




# List all published magazines
def defence_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Defence')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Defence')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Defence')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Defence')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Defence')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Defence')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Defence')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Defence')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'defense.html', context)




def defence_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'defense.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })






# List all published magazines
def mobility_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Mobility')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Mobility')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Mobility')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Mobility')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Mobility')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Mobility')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Mobility')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Mobility')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'mobility.html', context)



def mobility_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'mobility.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })






# List all published magazines
def logistics_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Logistics')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Logistics')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Logistics')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Logistics')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Logistics')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Logistics')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Logistics')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Logistics')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'logistics.html', context)



def logistics_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'logistics.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })




# List all published magazines
def fashion_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Fashion')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Fashion')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Fashion')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Fashion')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Fashion')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Fashion')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Fashion')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Fashion')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'fashion.html', context)



def fashion_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'fashion.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })




# List all published magazines
def media_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Media')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Media')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Media')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Media')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Media')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Media')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Media')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Media')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'media.html', context)



def media_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'media.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })





# List all published magazines
def cinema_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Cinema')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Cinema')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Cinema')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Cinema')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Cinema')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Cinema')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Cinema')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Cinema')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'cinema.html', context)


def cinema_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'cinema.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })




# List all published magazines
def startups_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Startups')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Startups')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Startups')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Startups')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Startups')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Startups')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Startups')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Startups')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'startups.html', context)


def startups_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'startups.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })





# List all published magazines
def investments_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Investments')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Investments')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Investments')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Investments')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Investments')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Investments')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Investments')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Investments')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'investments.html', context)


def investments_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'investments.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })




# List all published magazines
def news_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'News')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'News')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'News')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'News')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'News')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Defence')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'News')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'News')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'news_list.html', context)






def news_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'news.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })





# List all published magazines
def future_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Future')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Future')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Future')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Future')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Future')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Future')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Future')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Future')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'future_list.html', context)


def future_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'future.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })




# List all published magazines
def reviews_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Reviews')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Reviews')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Reviews')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Reviews')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Reviews')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Reviews')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Reviews')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Reviews')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'reviews_list.html', context)


def reviews_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'reviews.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })





# List all published magazines
def ratings_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Ratings')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Ratings')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Ratings')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Ratings')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Ratings')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Ratings')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Ratings')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Ratings')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'ratings_list.html', context)


def ratings_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'ratings.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })




# List all published magazines
def technologies_article(request):
    most_popular_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Technologies')).order_by('-published_at')[:1]
    latest_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Technologies')).order_by('-published_at')[:3]
    latest_magazines_3_5_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Technologies')).order_by('-published_at')[3:5]
    latest_magazines_5_8_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Technologies')).order_by('-published_at')[5:8]
    recent_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Technologies')).order_by('-published_at')[:5]
    old_magazines_list = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Technologies')).order_by('-published_at')[3:]
    archived = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Technologies')).order_by('-published_at')[5:9]

    all_magazine = Magazine.objects.filter(Q(is_published=True) & Q(category__name = 'Technologies')).order_by('-published_at')[0:]

    context = {
        "latest_magazines": latest_magazines_list,
        "old_magazines": old_magazines_list,
        "recent": recent_list,
        "latest_magazines_3_5": latest_magazines_3_5_list,
        "latest_magazines_5_8": latest_magazines_5_8_list,
        'most_popular':most_popular_list,
        'all_magazine':all_magazine,
        "archived":archived,
    }
    return render(request, 'technologies_list.html', context)


def technologies_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted

        if form_type == "subscription":  # If subscription form is submitted
            subscription_form = SubscriptionForm(request.POST)
            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Subscription successful! 🎉")
                else:
                    messages.warning(request, "You're already subscribed!")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'technologies.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })









def contact_Us(request):
    if request.method == "POST":

        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        message=request.POST.get('message')
        subject=request.POST.get('reason')

        print("subject=====", subject)

        contact=Contact_Us(name=name,email=email,phone=phone,message=message, subject=subject)
        contact.save()

    return render(request,'contact.html')





def About(request):
    return render (request,'about.html')




from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.db.models import Q

User = get_user_model()  # Ensure we use the correct user model

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user exists with the given email or username
        user = User.objects.filter(Q(email=email) | Q(username=username)).first()

        if user:
            # Authenticate the existing user
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect('/')  # Redirect to home/dashboard
            else:
                messages.error(request, "Incorrect password. Please try again.")
                return redirect('signup')  # Redirect back to login page

        else:
            # Create new user and log them in
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('/')  # Redirect to home/dashboard

    return render(request, 'signup.html')  # Render signup form



def user_logout(request):
    logout(request)
    return redirect('signup')




@csrf_exempt  # Only if you don't use {% csrf_token %} in the form
def subscribe(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data
            email = data.get("email", "").strip()

            if not email:
                return JsonResponse({"status": "error", "message": "Email is required!"}, status=400)

            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({"status": "error", "message": "You are already subscribed!"}, status=400)

            Subscriber.objects.create(email=email)
            return JsonResponse({"status": "success", "message": "Subscription successful!"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid data!"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request!"}, status=400)








def singlepage(request):
    return render(request,'book.html')


def search_list(request):
    return render(request,'search_list.html')




def subscribe(request):
    if request.method == "POST":
        email=request.POST.get('email')

        print("subject=====", email)

        contact=Subscriber(email=email)
        contact.save()
        return redirect('/')
    return render(request,'subscribe.html')