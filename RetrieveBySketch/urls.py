"""RetrieveBySketch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from retrieval import views as retrieval_views
from django.views import static as static_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', retrieval_views.register, name='register'),
    url(r'^login/$', retrieval_views.login, name='login'),
    url(r'^logout/$', retrieval_views.logout_view, name='logout'),
    url(r'^home/$', retrieval_views.home, name='home'),
    url(r'^load_home/$', retrieval_views.load_home, name='load_home'),
    url(r'^my_like/$', retrieval_views.my_like, name='my_like'),
    url(r'^my_up/$', retrieval_views.my_up, name='my_up'),
    url(r'^load_likes/$', retrieval_views.load_likes, name='load_likes'),
    url(r'^load_ups/$', retrieval_views.load_ups, name='load_ups'),
    url(r'^load_imgs/$', retrieval_views.load_imgs, name='load_imgs'),
    url(r'^load_1st_candice/$', retrieval_views.load_1st_candice, name='load_1st_candice'),
    url(r'^load_candice/$', retrieval_views.load_candice, name='load_candice'),
    url(r'^load_more/$', retrieval_views.load_more, name='load_more'),
    url(r'^change_candice/$', retrieval_views.change_candice, name='change_candice'),
    url(r'^select_candi/$', retrieval_views.select_candi, name='select_candi'),
    url(r'^unselect_candi/$', retrieval_views.unselect_candi, name='unselect_candi'),
    url(r'^like_img/$', retrieval_views.like_img, name='like_img'),
    url(r'^upload_imgs/$', retrieval_views.upload_imgs, name='upload_imgs'),
    url(r'^media/(?P<path>.*)$', static_views.serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
]
