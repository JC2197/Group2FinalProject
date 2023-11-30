"""
URL configuration for Group2Final project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from finalproject import views
from django.contrib.auth.views import LoginView
from finalproject.forms import BootstrapAuthenticationForm
from django.views.generic import RedirectView
from finalproject.views import signup


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', RedirectView.as_view(url='/signup/'), name='redirect_to_signup'),
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(
        authentication_form=BootstrapAuthenticationForm,
        template_name='login.html'
    ), name='login'),
    path('search-results/', views.search, name='search-results'),
    path('saved-events/', views.save_event, name='saved-events'),
]
