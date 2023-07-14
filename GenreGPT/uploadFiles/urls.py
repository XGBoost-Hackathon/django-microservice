from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('upload/', upload_files, name='upload_files'),
    path('pdf/', pdf_template, name='pdf'),
    path('input/', upload_text, name='input'),


    # path('filedetail/<int:pk>/', FileDetail.as_view(),name= 'file_detail'),   

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)