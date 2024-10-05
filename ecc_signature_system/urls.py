from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('digital_signatures/', include('digital_signatures.urls')),
    path('', lambda request: HttpResponseRedirect('digital_signatures/')),
]
