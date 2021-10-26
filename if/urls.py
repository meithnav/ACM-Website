from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    # path('pay/', views.initiate_payment, name='pay'),
    # path('callback/', views.callback, name='callback'),
    path('form/',views.closed_register,name='if_form'),
    # path('form2/',views.form,name='if_form2'),
    path('refundabcdefgh/',views.refund,name='refund'),
    path('refund_detailabcdefgh/<int:id>/',views.refund_detail,name='refund_detail'),
    # path('form3/',views.form3,name='if_form3'),
    path('excel_of_all/',views.export_excel_all,name='excel_for_all'),
    path('home/',views.if_home,name='if_home'),
    path('job_profile/',views.job_profile,name='job_profile'),
    path('job_single/<int:id>/',views.job_single,name='job_single'),
    path('changing/', views.changing)
    # path('core/register/16',views.form3,name='if_private')
]
