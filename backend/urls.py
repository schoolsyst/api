"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# Setup, imports...
from django.http import HttpResponse
from schedule.views import *
from homework.views import *
from learn.views import *
from common.views import *
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

api = DefaultRouter()

# ===================== API ROUTES ======================
# ---------------------- Common -------------------------
api.register(r'users', UserViewSet, 'users')
api.register(r'settings', SettingsViewSet, 'settings')
api.register(r'settings-definitions', SettingsDefinitionsViewSet, 'default_settings')
api.register(r'subjects', SubjectsViewSet, 'subjects')
# ----------------------- Learn -------------------------
api.register(r'notes', NotesViewSet, 'notes')
api.register(r'learndata', LearndataViewSet, 'learndata')
# --------------------- Schedule ------------------------
api.register(r'events', EventsViewSet, 'events')
api.register(r'events-mutations', MutationsViewSet, 'mutations')
# --------------------- Homework ------------------------
api.register(r'grades', GradesViewSet, 'grades')
api.register(r'homework', HomeworkViewSet, 'homework')

# Add to urlpatterns
urlpatterns = [
    path('api/users/self/', CurrentUserViewSet.as_view({'get': 'retrieve'})),
    path('api/auth/', obtain_jwt_token),
    path('api/auth/refresh/', refresh_jwt_token),
    path('api/auth/verify/', verify_jwt_token),
    path('api/auth/logout/', lambda req: HttpResponse('')),
    path('api/', include(api.urls)),
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('api-root')),
]
