
from django.conf import settings
from django.urls import path
from Magazine import views
from django.conf.urls.static import static



urlpatterns = [
    path("", views.home, name="home"),
    path('magazine/<slug:slug>/', views.magazine_detail, name='magazine_detail'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path("news",views.news_article,name='news_article'),
    path("contact",views.contact_Us, name='contact'),
    path("magazine_list",views.magazine_list,name='magazine_list'),
    path("defense",views.defense_article, name='defense_article'),
    path("mobility",views.mobility_article,name='mobility_article'),
    path("logistics",views.logistics_article,name='logistics_article'),
    path("fashion",views.fashion_article,name='fashion_article'),
    path("media",views.media_article,name='media_article'),
    path("cinema",views.cinema_article,name='cinema_article'),
    path("startups",views.startups_article,name='startups_article'),
    path("investments",views.investments_article,name='investments_article'),
    path("about",views.About,name='about'),
    path("subscribe", views.subscribe, name="subscribe"),  # Subscription API),
    path("singlepage",views.singlepage,name='singlepage'),
    path("signup", views.signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    # path('login/', login_view, name='login'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)