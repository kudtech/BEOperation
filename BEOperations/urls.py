
from django.contrib import admin

from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from beweb import forms, views
from datetime import datetime
from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='home'),
    path('api-token-auth/', obtain_auth_token,
         name='api_token_auth'),  # <-- And here
    path('beapi/', include('beapi.urls', namespace='beapi')),
    path('beweb/', include('beweb.urls', namespace='beweb')),
    # path('e117/', include('e117.urls', namespace='e117')),
    path('login/',
         LoginView.as_view
         (
             template_name='beweb/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context={
                 'note': 'Log in',
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('admin/', admin.site.urls, name="admin"),
    path('api-auth', include('rest_framework.urls')),
    url('^', include('django.contrib.auth.urls')),
    # url(r'^report_builder/', include('report_builder.urls'))
    # url(r'^api-token-auth/', obtain_auth_token)
]
