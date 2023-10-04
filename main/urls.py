
from django.urls import path
from django.conf.urls.static import static
from django.conf  import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from . views import *

urlpatterns = [
    path('',index,name='index'),
    path('home/',home,name="home"),
    path('add/',add,name='add-detail'),
    path('login/',loginn,name='login'),
    path('register/',register,name='register'),
    path('logout/',user_logout,name='logout'),
    path('income/',income,name='income'),
    path('new/',new,name='new'),
    path('add_category/',add_category_byuser,name='add_category'),
    path('delete/<int:id>/',delete,name='delete'),
    path('delete_income/<int:id>/',delete_income,name='delete_income'),
    path('update/<int:id>/',update,name='update'),
    path('income_update/<int:id>/',income_update,name='income_update'),
    path('graph/',graph,name='graph'),
    path('info/<int:month>',user_info,name='info'),
    path('date/',date_hist,name='date'),
    path('monthly_expense/',monthly_expense,name='monthly_expense'),
    path('yearly_expense/',yearly_expense,name='yearly_expense'),
    path('repeated/',repeated,name='repeated'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    # path('category/', category, name='category'),
    # path('delete_cat/<int:category_id>/',delete_cat, name='delete_cat'),

   

 
 

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
    
    urlpatterns += staticfiles_urlpatterns()