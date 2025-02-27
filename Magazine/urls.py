
from django.conf import settings
from django.urls import path
from Magazine import views
from django.conf.urls.static import static



urlpatterns = [
    path("", views.home, name="home"),
    path('magazine/<slug:slug>/', views.magazine_detail, name='magazine_detail'),
    path("contact",views.contact, name='contact'),    
    path("magazine_list",views.magazine_list,name='magazine_list'),
    path("about",views.About,name='about'),
    path("subscribe/", views.subscribe, name="subscribe"),  # Subscription API




    # path("singlepage",views.singlepage,name='singlepage'),
    # path("page",views.page,name='page'),  
    # path("page2",views.page2,name='page2'), 
    # path("subscribe", views.Subscribe, name='subscribe'),
    # path("future_military", views.future_military, name='future_military'),
    # path("AI_STARTUPS", views.AI_STARTUPS, name='AI_STARTUPS'),
    # path("PARADIGM", views.PARADIGM, name='PARADIGM'),
    #  path("next_unicorn", views.next_unicorn, name='next_unicorn'),
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)