"""training URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from apt import views
from django.contrib.auth import views as auth_views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$',views.Login, name="login"),
    #url(r'^$', views.log_out, name="logout"),

    url(r'^signup/$', views.signup, name="signup"),
    url(r'^about/$',views.about,name='about'),
    url(r'^contact/$',views.contact,name='contact'),
    url(r'^$',views.home,name='home'),
    url(r'^logsuccess/$',views.logsuccess,name='logsuccess'),
    url(r'^exam/$',views.exam,name='exam'),
    url(r'^startexam/$',views.startexam,name='startexam'),
    url(r'^Assignment/$', views.Assignmentview,name='Assignment'),
    url(r'^home-work/$',views.infoview, name='home-work'),
    url(r'^written_exam/$',views.written_exam,name='written_exam'),
    url(r'^attendance_update/$',views.attendance_update, name='attendance_update'),
    url(r'^exam-results/$',views.result_view, name='exam-results'),
    url(r'^attend-view/$',views.attendanceView, name='attendance-view'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
