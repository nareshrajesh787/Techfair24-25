"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from home import views as home_views
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name='home'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('register/', user_views.register_view, name='register'),
    path('dashboard/', user_views.dashboard, name='dashboard'),

    path('upload_assignment/', home_views.upload_assignment, name='upload_assignment'),
    path('assignment/<int:pk>/', home_views.DetailView, name='detail'),
    path('assignment/<int:pk>/update/', home_views.update_assignment, name='update_assignment'),
    path('assignment/<int:pk>/delete/', home_views.delete_assignment, name='delete_assignment'),
    path('assignment/<int:pk>/define-rubric/', home_views.define_rubric, name='define_rubric'),
    path('assignment/<int:pk>/update-rubric/', home_views.update_rubric, name='update_rubric'),

    path('review/<int:pk>/', home_views.ReviewDetail, name='review_detail'),
    path('assignment/<int:pk>/review', home_views.SubmitReview, name='review_form'),
    path('review/<int:pk>/update/', home_views.update_review, name='update_review'),
    path('review/<int:pk>/delete/', home_views.delete_review, name='delete_review'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
