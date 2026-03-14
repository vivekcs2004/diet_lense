"""
URL configuration for dietlense project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from diet_app.views import (SignUpView,UserProfileCreateView,UserProfileRetrieveUpdateView,
                            UserDetailsView,FoodLogCreateListView,
                            FoodLogUpdateRetrieveDeleteView,DailySummaryView,
                            GetDietPlanView,AnalyzeFoodImageView)
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',SignUpView.as_view()),
    path('token/',ObtainAuthToken.as_view()),
    path('profile/',UserProfileCreateView.as_view()),
    path('profile/<int:pk>/',UserProfileRetrieveUpdateView.as_view()),
    path('profile/<int:pk>/update/',UserProfileRetrieveUpdateView.as_view()),
    path('user/<int:pk>/',UserDetailsView.as_view()),
    path('foodlog/',FoodLogCreateListView.as_view()),
    path('foodlog/<int:pk>/',FoodLogUpdateRetrieveDeleteView.as_view()),
    path('summary/',DailySummaryView.as_view()),
    path('diet-plan/',GetDietPlanView.as_view()),
    path('analyze-image/',AnalyzeFoodImageView.as_view()),
    
]
