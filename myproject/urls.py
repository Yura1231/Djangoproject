"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import register , login ,delete_event ,user_commentsss ,   get_profile ,   update_profile ,  create_event , user_events  , get_events , check_event_registration , subscribe_to_post , unsubscribe , my_subscriptions , send_subscription_email ,confirm_subscription ,get_user_profile , user_comments
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', get_profile, name='login'),
    path('update-profile/', update_profile, name='update-profile'),
    path('create-event/', create_event, name='create_event'),
    path('my-events/', user_events, name='list_all_events'),
    path('events/', get_events, name='events-list'),
    path('events/<int:event_id>/check-registration/', check_event_registration, name='check_event_registration'),
    path('events/<int:event_id>/', subscribe_to_post, name='subscribe_to_post'),
    path('unsubscribe/<int:event_id>/', unsubscribe, name='unsubscribe'),
    path('my-subscriptions/', my_subscriptions, name='my_subscriptions'),
    path("subscribe/<int:event_id>/", send_subscription_email, name="subscribe_email"),
    path("confirm-subscription/<str:token>/", confirm_subscription, name="confirm_subscription"),
    path("profile/<int:user_id>/", get_user_profile, name="get_user_profile"),
    path("comments/<int:user_id>/", user_comments, name="user-comments"),
    path('delete/<int:event_id>/', delete_event, name='delete_event'),
    
    path('comments/', user_commentsss, name='user_commentsss'),
   
   
]  




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)