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
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

api = DefaultRouter()
from users.views    import *
from common.views   import *
from learn.views    import *
from schedule.views import *

# ===================== API ROUTES ======================
# ----------------------- Users -------------------------
api.register(r'users',     UserViewSet,      'users')
# ---------------------- Common -------------------------
api.register(r'settings',  SettingsViewSet,  'settings')
api.register(r'subjects',  SubjectsViewSet,  'subjects')
# ----------------------- Learn -------------------------
api.register(r'notions',   NotionsViewSet,   'notions')
api.register(r'tests',     TestsViewSet,     'tests')
api.register(r'notes',     NotesViewSet,     'notes')
api.register(r'grades',    GradesViewSet,    'grades')
# --------------------- Schedule ------------------------
api.register(r'events',    EventsViewSet,    'events')
api.register(r'additions', AdditionsViewSet, 'additions')
api.register(r'deletions', DeletionsViewSet, 'deletions')
api.register(r'exercises', ExercisesViewSet, 'exercises')


# Add to urlpatterns
urlpatterns = [
    path('api/auth/', obtain_jwt_token),
    path('api/auth/refresh/', refresh_jwt_token),
    path('api/auth/verify/', verify_jwt_token),

    path('api/', include(api.urls)),
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('api-root')),
]
