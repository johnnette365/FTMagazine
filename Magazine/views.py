from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from Magazine.models import Magazine, Comment, Subscriber
from Magazine.forms import CommentForm, SubscriptionForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def home(request):
    query = request.GET.get('q')  # Get search query from the request

    if query:
        # Filter magazines by title or content based on search query
        latest_magazines = Magazine.objects.filter(title__icontains=query, is_published=True).order_by('-published_at')[:2]
        recent = Magazine.objects.filter(title__icontains=query, is_published=True).order_by('-published_at')[:5]
        old_magazines = Magazine.objects.filter(title__icontains=query, is_published=True).order_by('-published_at')[2:]
    else:
        # Default query when no search is performed
        latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:2]
        recent = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
        old_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[2:]

    context = {
        "latest_magazines": latest_magazines,
        "old_magazines": old_magazines,
        "recent": recent,
        "query": query,  # Pass query back to template to show in search field
    }
    return render(request, "home.html", context)

# def home(request):
#     latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:2]
#     recent = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
#     old_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[2:]

    
    # context={
    #     "latest_magazines":latest_magazines,
    #     "old_magazines":old_magazines,
    #     "recent":recent,
    # }
    # return render(request, "home.html", context)



# List all published magazines
def magazine_list(request):
    magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'magazine_list.html', {'magazines': magazines})



def magazine_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    # Initialize forms
    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Identify which form was submitted
        print('lets see =========',  form_type)

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

        if form_type == "comment":  # If comment form is submitted
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.magazine = magazine
                comment.user = request.user  # Ensure user is logged in
                comment.created_at = timezone.now()
                comment.save()
                messages.success(request, "Comment added successfully! ✍️")
                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'magazine.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })



def contact(request):
    return render(request,'contact.html')


def magazine_list(request):
    return render(request, 'magazine_list.html')


def About(request):
    return render (request,'about.html')





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
    return render(request,'singlepage.html')


def page(request):
    return render (request,'page.html')

def page2(request):
    return render (request,'page2.html')




def Subscribe(request):
    return render(request,'subscribe.html')


def future_military(request):
    return render(request,'future_military.html')


def AI_STARTUPS(request):
    return render(request,'AI_STARTUPS.html')

def PARADIGM(request):
    return render(request,'PARADIGM.html')

def next_unicorn(request):
    return render(request,'next_unicorn.html')