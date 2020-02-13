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
from reports.views import *
from django.contrib import admin
from django.urls import path, include, register_converter
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
# ---------------------- Reports ------------------------
api.register(r'reports', ReportsViewSet, 'reports')

# Custom ISO 8601 path param type converter
class ISO8601Converter:
    import dateutil
    regex = r'^(?:[1-9]\d{3}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1\d|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[1-9]\d(?:0[48]|[2468][048]|[13579][26])|(?:[2468][048]|[13579][26])00)-02-29)(?:T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:Z|[+-][01]\d:[0-5]\d))?$'  # Yes, this is monstruous.

    def to_python(self, value):
        fmt = 'datetime' if 'T' in value else 'date'
        value = dateutil.parser.isoparse(value)
        return (fmt, value)

    def to_url(self, value):
        fmt, dt = value
        dt.isoformat(value)

register_converter(ISO8601Converter, 'datetime')

# Add to urlpatterns
urlpatterns = [
    path('api/users/self/', CurrentUserViewSet.as_view({'get': 'retrieve'})),
    path('api/auth/', obtain_jwt_token),
    path('api/auth/refresh/', refresh_jwt_token),
    path('api/auth/verify/', verify_jwt_token),
    path('api/auth/logout/', lambda req: HttpResponse('')),
    path('api/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/courses/<start>/<end>/', EventsViewSet.as_view({"get": "courses"})),
    path('api/notes/convert/<slug:uuid_or_in_format>/<slug:out_format>/', NotesViewSet.as_view({"post": "convert", "get": "convert"})),
    path('api/', include(api.urls)),
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('api-root')),
]
