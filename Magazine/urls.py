
from django.conf import settings
from django.urls import path
from Magazine import views
from django.conf.urls.static import static



urlpatterns = [
    path("", views.home, name="home"),
    path("magazine_list",views.magazine_list,name='magazine_list'),
    path('magazine/<slug:slug>/', views.magazine_detail, name='magazine_detail'),

    path("news",views.news_article,name='news_article'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),

    path("future",views.future_article,name='future_list'),
    path('future/<slug:slug>/', views.future_detail, name='future_detail'),

    path("reviews",views.reviews_article,name='reviews_list'),
    path('reviews/<slug:slug>/', views.reviews_detail, name='reviews_detail'),

    path("ratings",views.ratings_article,name='ratings_list'),
    path('ratings/<slug:slug>/', views.ratings_detail, name='ratings_detail'),

    path("technologies",views.technologies_article,name='technologies_list'),
    path('technologies/<slug:slug>/', views.technologies_detail, name='technologies_detail'),

    path("defence",views.defence_article, name='defence_article'),
    path('defence/<slug:slug>/', views.defence_detail, name='defence_detail'),


    path("mobility",views.mobility_article,name='mobility_article'),
    path('mobility/<slug:slug>/', views.mobility_detail, name='mobility_detail'),

    path("logistics",views.logistics_article,name='logistics_article'),
    path('logistics/<slug:slug>/', views.logistics_detail, name='logistics_detail'),

    path("fashion",views.fashion_article,name='fashion_article'),
    path('fashion/<slug:slug>/', views.fashion_detail, name='fashion_detail'),

    path("media",views.media_article,name='media_article'),
    path('media/<slug:slug>/', views.media_detail, name='media_detail'),

    path("cinema",views.cinema_article,name='cinema_article'),
    path('cinema/<slug:slug>/', views.cinema_detail, name='cinema_detail'),

    path("startups",views.startups_article,name='startups_article'),
    path('startups/<slug:slug>/', views.startups_detail, name='startups_detail'),

    path("investments",views.investments_article,name='investments_article'),
    path('investments/<slug:slug>/', views.investments_detail, name='investments_detail'),


    path("contact",views.contact_Us, name='contact'),
    path("about",views.About,name='about'),
    path("subscribe", views.subscribe, name="subscribe"),  # Subscription API),
    path("singlepage",views.singlepage,name='singlepage'),
    path("signup", views.signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('search_list', views.search_list, name='search_list'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)