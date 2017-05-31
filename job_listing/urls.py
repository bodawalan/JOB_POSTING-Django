from django.conf.urls import url,include
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
   # url(r'^home/$',views.home ,name='home'),
    #url(r'^home/suggest',views.suggestion_view,name='suggestion'),
    url(r'^$',  views.fill_form,name='fillform'),
    url(r'^login/job_opening',views.job_opening,name='job_opening'),
    url(r'^suggestion_view',views.suggestion_view,name='suggestion_view'),
    #url(r'^accounts/', include('allauth.urls')),
    url(r'^register/$', views.RegisterView.as_view(), name = 'register'),
    url(r'^login/$', views.LoginView.as_view(), name = 'login'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^logout/$', views.LogoutView.as_view(), name = 'logout'),
    url(r'^login/dashboard/$', views.DashboardView.as_view(), name = 'dashboard'),
    url(r'^register/dashboard/$', views.DashboardView.as_view(), name = 'dashboard'),

    #url(r'',views.job_posting,name='jobposting')


]